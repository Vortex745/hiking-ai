"""Agent tests for the OpenManus-only execution path."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from langchain_core.messages import AIMessage


def collect_async(async_iterable):
    async def _collect():
        return [event async for event in async_iterable]

    return asyncio.run(_collect())


class FakeToolModel:
    def __init__(self, responses):
        self.responses = list(responses)
        self.bound_tools = []
        self.messages = []

    def bind_tools(self, tools, tool_choice="auto"):
        self.bound_tools = tools
        self.tool_choice = tool_choice
        return self

    def invoke(self, messages):
        self.messages = messages
        if self.responses:
            return self.responses.pop(0)
        return AIMessage(content="任务已完成。")


def _fake_tool(name: str, result: str = "ok"):
    tool = SimpleNamespace()
    tool.name = name
    tool.description = f"{name} fake tool"
    tool.ainvoke = AsyncMock(return_value=result)
    return tool


def _tool_call_response(tool_name: str, args: dict, call_id: str = "call-1"):
    return AIMessage(
        content="",
        tool_calls=[{"name": tool_name, "args": args, "id": call_id}],
    )


def _run_with_tool(monkeypatch, tool_name: str, args: dict):
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    monkeypatch.setattr("agent.agent.settings.mcp_servers", {})
    fake_llm = FakeToolModel([
        _tool_call_response(tool_name, args),
        AIMessage(content="完成。"),
    ])

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent import agent as agent_module
        from agent.agent import AIAgent

        if tool_name != "unknown_tool":
            fake_tool = _fake_tool(tool_name, f"{tool_name} result")
            monkeypatch.setitem(agent_module.AVAILABLE_TOOL_MAP, tool_name, fake_tool)
            monkeypatch.setattr(agent_module, tool_name, fake_tool, raising=False)

        return collect_async(AIAgent().aexecute_stream("test"))


def test_get_tool_registry_returns_tool_registry_instance():
    from agent.agent import AIAgent
    from tools.tool_registry import ToolRegistry

    assert isinstance(AIAgent.get_tool_registry(), ToolRegistry)


def test_get_tool_registry_has_expected_tools():
    from agent.agent import AIAgent

    names = {tool.name for tool in AIAgent.get_tool_registry().list_all_tools()}

    assert "web_search" in names
    assert "weather_lookup" not in names
    assert "geo_lookup" not in names
    assert "mcp_amap_maps_weather" not in names
    assert "terminate" in names


def test_openmanus_tool_call_metadata_has_risk_fields(monkeypatch):
    events = _run_with_tool(monkeypatch, "web_search", {"query": "test"})

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]

    assert meta["runtime"] == "openmanus"
    assert meta["tool"] == "web_search"
    assert meta["risk_level"] == "low"
    assert meta["needs_confirmation"] is False


def test_openmanus_medium_risk_tool_metadata(monkeypatch):
    events = _run_with_tool(monkeypatch, "web_scraping", {"url": "http://example.com"})

    tool_call = next(e for e in events if e["type"] == "tool_call")

    assert tool_call["metadata"]["risk_level"] == "medium"
    assert tool_call["metadata"]["needs_confirmation"] is False


def test_openmanus_high_risk_tool_emits_approval_required(monkeypatch):
    events = _run_with_tool(
        monkeypatch,
        "file_operation",
        {"operation": "create", "path": "/tmp/test"},
    )

    tool_call = next(e for e in events if e["type"] == "tool_call")
    approval = next(e for e in events if e["type"] == "approval_required")

    assert tool_call["metadata"]["risk_level"] == "high"
    assert tool_call["metadata"]["needs_confirmation"] is True
    assert approval["metadata"]["tool"] == "file_operation"


def test_openmanus_critical_risk_tool_metadata(monkeypatch):
    events = _run_with_tool(monkeypatch, "terminal", {"command": "ls"})

    tool_call = next(e for e in events if e["type"] == "tool_call")
    approval = next(e for e in events if e["type"] == "approval_required")

    assert tool_call["metadata"]["risk_level"] == "critical"
    assert approval["metadata"]["needs_confirmation"] is True


def test_unknown_tool_falls_back_to_medium_risk(monkeypatch):
    events = _run_with_tool(monkeypatch, "unknown_tool", {})

    tool_call = next(e for e in events if e["type"] == "tool_call")
    tool_result = next(e for e in events if e["type"] == "tool_result")

    assert tool_call["metadata"]["risk_level"] == "medium"
    assert "Unknown tool" in tool_result["content"]


def test_openmanus_start_exposes_raw_mcp_tools_without_intent_gate(monkeypatch):
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

    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    monkeypatch.setattr("agent.agent.settings.mcp_servers", {
        "amap": {
            "command": "cmd",
            "args": ["/c", "amap"],
            "env": {"AMAP_MAPS_API_KEY": "test"},
        }
    })
    monkeypatch.setattr("agent.mcp_tools.MCPClient", FakeMCPClient)
    fake_llm = FakeToolModel([AIMessage(content="直接回答。")])

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent.agent import AIAgent

        events = collect_async(AIAgent().aexecute_stream("明晚广州什么天气", scenario="weather"))

    start = next(e for e in events if e.get("metadata", {}).get("phase") == "openmanus_start")
    tools = start["metadata"]["tools"]

    assert "mcp_amap_maps_weather" in tools
    assert "weather_lookup" not in tools
    assert "geo_lookup" not in tools
    assert ("initialize",) in calls
    assert ("close",) in calls


def test_openmanus_prompt_does_not_reference_removed_weather_aliases(monkeypatch):
    class FakeMCPClient:
        def __init__(self):
            self.process = object()
            self.tools = {}

        async def connect_stdio(self, command, args=None, env=None):
            pass

        async def initialize(self):
            return {}

        async def list_tools(self):
            self.tools["maps_weather"] = {
                "name": "maps_weather",
                "description": "Query AMap weather",
                "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}}},
            }
            return list(self.tools.values())

        async def call_tool(self, tool_name, arguments=None):
            return [{"type": "text", "text": "晴"}]

        async def close(self):
            pass

    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    monkeypatch.setattr("agent.agent.settings.mcp_servers", {
        "amap": {"command": "cmd", "args": ["/c", "amap"]}
    })
    monkeypatch.setattr("agent.mcp_tools.MCPClient", FakeMCPClient)
    fake_llm = FakeToolModel([AIMessage(content="直接回答。")])

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent.agent import AIAgent

        collect_async(AIAgent().aexecute_stream("明晚广州什么天气", scenario="weather"))

    system_prompt = getattr(fake_llm.messages[0], "content", "")

    assert "mcp_amap_maps_weather" in system_prompt
    assert "weather_lookup" not in system_prompt
    assert "geo_lookup" not in system_prompt


def test_system_prompt_no_hardcoded_mcp_tool_names():
    """Prompt rules must be generic — no specific MCP tool names in Constraints or DecisionPolicy."""
    from agent.prompts import SYSTEM_PROMPT, NEXT_STEP_PROMPT

    # Constraints and DecisionPolicy should NOT contain specific MCP tool names
    for section in [SYSTEM_PROMPT, NEXT_STEP_PROMPT]:
        assert "mcp_pexels" not in section, (
            "Hardcoded MCP tool name found in prompt — use generic rules instead"
        )


def test_system_prompt_has_generic_tool_required_rule():
    """Prompt must have a generic rule: when content requires a tool, call it, don't say 'cannot provide'."""
    from agent.prompts import SYSTEM_PROMPT, NEXT_STEP_PROMPT

    # Must contain a generic rule about content that requires tools
    assert "不得" in SYSTEM_PROMPT and "无法提供" in SYSTEM_PROMPT, (
        "Missing generic rule: must call tools for content types that require them"
    )
    assert "不得" in NEXT_STEP_PROMPT, (
        "DecisionPolicy missing generic rule about tool-required content"
    )


def test_pexels_markdown_preview_is_appended_to_final_answer(monkeypatch):
    class FakeMCPClient:
        def __init__(self):
            self.process = object()
            self.tools = {}

        async def connect_stdio(self, command, args=None, env=None):
            pass

        async def initialize(self):
            return {}

        async def list_tools(self):
            self.tools["search_photos"] = {
                "name": "search_photos",
                "description": "Search Pexels photos",
                "inputSchema": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            }
            return list(self.tools.values())

        async def call_tool(self, tool_name, arguments=None):
            return [{
                "type": "text",
                "text": json.dumps({
                    "provider": "Pexels",
                    "photos": [{
                        "markdown_preview": "![Forbidden City](https://images.pexels.com/photos/1/medium.jpeg)",
                        "url": "https://www.pexels.com/photo/1/",
                    }],
                }),
            }]

        async def close(self):
            pass

    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    monkeypatch.setattr("agent.agent.settings.mcp_servers", {
        "pexels": {"command": "python", "args": ["pexels_server.py"]},
    })
    monkeypatch.setattr("agent.mcp_tools.MCPClient", FakeMCPClient)
    fake_llm = FakeToolModel([
        _tool_call_response("mcp_pexels_search_photos", {"query": "故宫"}),
        AIMessage(content="这里有一张故宫图片。"),
    ])

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent.agent import AIAgent

        events = collect_async(AIAgent().aexecute_stream("给我一张故宫的图片"))

    final_text = next(e for e in events if e["type"] == "text")["content"]

    assert "这里有一张故宫图片" in final_text
    assert "![Forbidden City](https://images.pexels.com/photos/1/medium.jpeg)" in final_text
