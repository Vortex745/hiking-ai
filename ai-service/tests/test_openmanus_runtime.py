from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from agent.base_agent import BaseAgent, OpenManusAgentState
from agent.hiking_manus import HikingManus
from agent.planning_flow import PlanStepStatus, PlanningFlow, PlanningTool
from agent.tool_call_agent import ToolCallAgent
from agent.tool_collection import ToolCollection


class EchoAgent(BaseAgent):
    async def step(self) -> str:
        self.update_memory("assistant", "done")
        self.state = OpenManusAgentState.FINISHED
        return "done"


def test_base_agent_run_uses_step_loop():
    agent = EchoAgent(name="echo", max_steps=3)

    result = asyncio.run(agent.run("hello"))

    assert "Step 1: done" in result
    assert agent.current_step == 1
    assert agent.state == OpenManusAgentState.FINISHED


def test_tool_collection_exposes_langchain_tools_and_params():
    @tool
    async def weather_lookup(destination: str) -> str:
        """Look up weather."""
        return f"{destination}: 晴"

    collection = ToolCollection(weather_lookup)

    assert collection.get_tool("weather_lookup") is weather_lookup
    assert collection.to_langchain_tools() == [weather_lookup]
    assert collection.to_params()[0]["function"]["name"] == "weather_lookup"


def test_tool_collection_executes_async_langchain_tool():
    @tool
    async def weather_lookup(destination: str) -> str:
        """Look up weather."""
        return f"{destination}: 晴"

    collection = ToolCollection(weather_lookup)

    result = asyncio.run(collection.execute(name="weather_lookup", tool_input={"destination": "北京"}))

    assert result.ok is True
    assert result.output == "北京: 晴"


def test_tool_call_agent_executes_tool_and_terminate_sets_finished():
    @tool
    async def terminate(reason: str = "done") -> str:
        """Terminate the task."""
        return f"原因: {reason}"

    class FakeLLM:
        async def ask_tool(self, **kwargs):
            return SimpleNamespace(
                content="",
                tool_calls=[
                    {
                        "id": "call-1",
                        "name": "terminate",
                        "args": {"reason": "任务完成"},
                    }
                ],
            )

    agent = ToolCallAgent(
        llm=FakeLLM(),
        available_tools=ToolCollection(terminate),
        special_tool_names=["terminate"],
    )

    result = asyncio.run(agent.run("结束"))

    assert "terminate" in result
    assert "任务完成" in result
    assert agent.state == OpenManusAgentState.FINISHED


def test_tool_call_agent_sends_legacy_function_history_to_legacy_provider():
    @tool
    async def weather_lookup(destination: str) -> str:
        """Look up weather."""
        return f"{destination}: 晴，适合徒步"

    class LegacyFunctionOnlyModel:
        def __init__(self):
            self.calls = 0

        def bind_tools(self, tools, tool_choice="auto"):
            return self

        def invoke(self, messages):
            self.calls += 1
            if self.calls == 1:
                return AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "weather_lookup",
                            "args": {"destination": "北京"},
                            "id": "call-weather-1",
                        }
                    ],
                )

            if any(getattr(message, "type", "") == "tool" for message in messages):
                raise ValueError("messages[3].role: unknown variant `tool`, expected `function`")

            assert any(
                getattr(message, "type", "") == "function" and getattr(message, "name", "") == "weather_lookup"
                for message in messages
            )
            assert not any(getattr(message, "type", "") == "tool" for message in messages)
            assert not any(
                getattr(message, "additional_kwargs", {}).get("tool_calls")
                for message in messages
                if getattr(message, "type", "") == "ai"
            )
            assert any(
                getattr(message, "additional_kwargs", {}).get("function_call", {}).get("name") == "weather_lookup"
                for message in messages
                if getattr(message, "type", "") == "ai"
            )
            return AIMessage(content="北京今天适合成熟短线徒步。")

    model = LegacyFunctionOnlyModel()
    agent = ToolCallAgent(
        llm=model,
        available_tools=ToolCollection(weather_lookup),
        max_steps=3,
    )

    result = asyncio.run(agent.run("北京今天适合徒步吗"))

    assert "北京今天适合成熟短线徒步" in result


def test_tool_call_agent_sends_standard_tool_history_to_tool_provider():
    @tool
    async def weather_lookup(destination: str) -> str:
        """Look up weather."""
        return f"{destination}: 晴，适合徒步"

    class StandardToolOnlyModel:
        def __init__(self):
            self.calls = 0

        def bind_tools(self, tools, tool_choice="auto"):
            return self

        def invoke(self, messages):
            self.calls += 1
            if self.calls == 1:
                return AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "weather_lookup",
                            "args": {"destination": "北京"},
                            "id": "call-weather-1",
                        }
                    ],
                )

            assert any(
                getattr(message, "type", "") == "tool" and getattr(message, "tool_call_id", "") == "call-weather-1"
                for message in messages
            )
            assert not any(getattr(message, "type", "") == "function" for message in messages)
            assert any(
                getattr(message, "type", "") == "ai"
                and getattr(message, "tool_calls", None)
                and message.tool_calls[0]["name"] == "weather_lookup"
                for message in messages
            )
            return AIMessage(content="北京今天适合成熟短线徒步。")

    model = StandardToolOnlyModel()
    agent = ToolCallAgent(
        llm=model,
        available_tools=ToolCollection(weather_lookup),
        max_steps=3,
    )

    result = asyncio.run(agent.run("北京今天适合徒步吗"))

    assert "北京今天适合成熟短线徒步" in result


def test_hiking_manus_create_wraps_tools_in_collection():
    fake_llm = object()
    fake_tool = SimpleNamespace(name="weather_lookup", description="weather", ainvoke=AsyncMock())

    manus = asyncio.run(HikingManus.create(llm=fake_llm, tools=[fake_tool], max_steps=5))

    assert manus.llm is fake_llm
    assert manus.max_steps == 5
    assert manus.available_tools.get_tool("weather_lookup") is fake_tool


def test_hiking_manus_initializes_mcp_tools_before_think(monkeypatch):
    calls = []

    class FakeMCPClient:
        def __init__(self):
            self.process = object()
            self.tools = {}

        async def connect_stdio(self, command, args=None, env=None):
            calls.append(("connect", command, args, env))

        async def initialize(self):
            calls.append(("initialize",))
            return {}

        async def list_tools(self):
            calls.append(("list_tools",))
            self.tools["maps_weather"] = {
                "name": "maps_weather",
                "description": "Query AMap weather",
                "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}}},
            }
            return list(self.tools.values())

        async def call_tool(self, tool_name, arguments=None):
            calls.append(("call_tool", tool_name, arguments))
            return [{"type": "text", "text": "晴"}]

        async def close(self):
            calls.append(("close",))

    monkeypatch.setattr("agent.mcp_tools.MCPClient", FakeMCPClient)

    manus = asyncio.run(HikingManus.create(
        llm=object(),
        tools=[],
        mcp_server_configs={
            "amap": {
                "command": "cmd",
                "args": ["/c", "amap"],
                "env": {"AMAP_MAPS_API_KEY": "test"},
            }
        },
    ))

    try:
        mcp_tool = manus.available_tools.get_tool("mcp_amap_maps_weather")
        assert mcp_tool is not None
        assert getattr(mcp_tool, "original_name") == "maps_weather"
        assert calls[:3] == [
            ("connect", "cmd", ["/c", "amap"], {"AMAP_MAPS_API_KEY": "test"}),
            ("initialize",),
            ("list_tools",),
        ]
    finally:
        asyncio.run(manus.cleanup())


def test_hiking_manus_initializes_http_mcp_tools(monkeypatch):
    calls = []

    class FakeMCPClient:
        def __init__(self):
            self.process = None
            self.http_url = None
            self.tools = {}

        @property
        def connected(self):
            return bool(self.http_url)

        async def connect_http(self, url, headers=None):
            calls.append(("connect_http", url, headers))
            self.http_url = url

        async def initialize(self):
            calls.append(("initialize",))
            return {}

        async def list_tools(self):
            calls.append(("list_tools",))
            self.tools["maps_weather"] = {
                "name": "maps_weather",
                "description": "Query AMap weather",
                "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}}},
            }
            return list(self.tools.values())

        async def call_tool(self, tool_name, arguments=None):
            calls.append(("call_tool", tool_name, arguments))
            return [{"type": "text", "text": "晴"}]

        async def close(self):
            calls.append(("close",))

    monkeypatch.setattr("agent.mcp_tools.MCPClient", FakeMCPClient)

    manus = asyncio.run(HikingManus.create(
        llm=object(),
        tools=[],
        mcp_server_configs={
            "amap": {"url": "https://mcp.amap.com/mcp?key=secret"},
        },
    ))
    try:
        mcp_tool = manus.available_tools.get_tool("mcp_amap_maps_weather")
        assert mcp_tool is not None
        assert getattr(mcp_tool, "original_name") == "maps_weather"
        assert ("connect_http", "https://mcp.amap.com/mcp?key=secret", None) in calls
    finally:
        asyncio.run(manus.cleanup())


def test_raw_mcp_tool_executes_through_original_server_tool(monkeypatch):
    calls = []

    class FakeMCPClient:
        def __init__(self):
            self.process = object()
            self.tools = {}

        async def connect_stdio(self, command, args=None, env=None):
            calls.append(("connect", command, args, env))

        async def initialize(self):
            calls.append(("initialize",))
            return {}

        async def list_tools(self):
            self.tools["maps_weather"] = {
                "name": "maps_weather",
                "description": "Query AMap weather",
                "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}}},
            }
            return list(self.tools.values())

        async def call_tool(self, tool_name, arguments=None):
            calls.append(("call_tool", tool_name, arguments))
            return [{"type": "text", "text": "广州 晴"}]

        async def close(self):
            calls.append(("close",))

    monkeypatch.setattr("agent.mcp_tools.MCPClient", FakeMCPClient)

    manus = asyncio.run(HikingManus.create(
        llm=object(),
        tools=[],
        mcp_server_configs={"amap": {"command": "cmd", "args": ["/c", "amap"]}},
    ))

    try:
        result = asyncio.run(manus.execute_tool("mcp_amap_maps_weather", {"city": "广州"}))
    finally:
        asyncio.run(manus.cleanup())

    assert ("call_tool", "maps_weather", {"city": "广州"}) in calls
    assert "广州 晴" in result


def test_planning_tool_tracks_step_status():
    planning = PlanningTool()

    asyncio.run(planning.execute("create", plan_id="plan_1", title="测试计划", steps=["A", "B"]))
    asyncio.run(
        planning.execute(
            "mark_step",
            plan_id="plan_1",
            step_index=0,
            step_status=PlanStepStatus.COMPLETED.value,
        )
    )

    plan = planning.plans["plan_1"]
    assert plan["step_statuses"] == ["completed", "not_started"]


def test_planning_flow_executes_first_active_step():
    agent = EchoAgent(name="echo")
    flow = PlanningFlow(agent=agent, active_plan_id="plan_1")
    asyncio.run(flow.create_plan("计划", ["第一步", "第二步"]))

    result = asyncio.run(flow.execute_next())

    assert "Step 1: done" in result
    assert flow.planning_tool.plans["plan_1"]["step_statuses"][0] == "completed"


def test_ai_agent_builds_hiking_manus_tool_collection(monkeypatch):
    monkeypatch.setattr("config.settings.memory_enabled", False)

    with patch("agent.agent.ChatOpenAI", return_value=object()):
        from agent import agent as agent_module
        from agent.agent import AIAgent
        from agent.intake import understand_request

        monkeypatch.setattr(agent_module.settings, "mcp_servers", {})
        agent = AIAgent()
        context = understand_request("随便聊聊")
        manus = asyncio.run(agent._build_hiking_manus(context))

    assert manus.llm is agent.llm
    assert manus.available_tools.to_langchain_tools()
    assert all(hasattr(item, "name") for item in manus.available_tools.to_langchain_tools())
