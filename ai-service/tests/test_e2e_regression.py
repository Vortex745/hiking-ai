"""End-to-end regressions for the OpenManus-only Agent path."""

from __future__ import annotations

import asyncio
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

    def bind_tools(self, tools, tool_choice="auto"):
        self.tools = tools
        return self

    def invoke(self, messages):
        if self.responses:
            return self.responses.pop(0)
        return AIMessage(content="任务已完成。")


def _fake_tool(name: str, result: str):
    return SimpleNamespace(
        name=name,
        description=f"{name} fake tool",
        ainvoke=AsyncMock(return_value=result),
    )


def _run_agent(monkeypatch, responses, tools=None, message="你好"):
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    fake_llm = FakeToolModel(responses)

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent import agent as agent_module
        from agent.agent import AIAgent

        has_legacy_langgraph_entrypoint = hasattr(agent_module, "create_react_agent")
        for tool_name, result in (tools or {}).items():
            fake_tool = _fake_tool(tool_name, result)
            monkeypatch.setitem(agent_module.AVAILABLE_TOOL_MAP, tool_name, fake_tool)
            monkeypatch.setattr(agent_module, tool_name, fake_tool, raising=False)

        events = collect_async(AIAgent().aexecute_stream(message))

    return events, has_legacy_langgraph_entrypoint


def test_greeting_runs_openmanus_direct_text(monkeypatch):
    events, has_legacy_langgraph_entrypoint = _run_agent(monkeypatch, [AIMessage(content="你好！我是 AI Hiking 助手。")])

    assert has_legacy_langgraph_entrypoint is False
    assert events[-1]["metadata"]["runtime"] == "openmanus"
    assert events[-1]["metadata"]["lane"] == "react"
    assert not [event for event in events if event["type"] == "tool_call"]


def test_weather_query_can_use_openmanus_tools(monkeypatch):
    events, _ = _run_agent(
        monkeypatch,
        [
            AIMessage(content="", tool_calls=[{"name": "weather_lookup", "args": {"destination": "北京"}, "id": "call-1"}]),
            AIMessage(content="北京晴，适合成熟短线徒步。"),
        ],
        tools={"weather_lookup": "北京晴，23°C，风力 3 级"},
        message="北京今天适合徒步吗",
    )

    assert any(event["type"] == "tool_call" and event["metadata"]["tool"] == "weather_lookup" for event in events)
    assert any(event["type"] == "tool_result" for event in events)
    assert events[-1]["metadata"]["status"] == "completed"


def test_route_planning_uses_same_openmanus_react_loop(monkeypatch):
    events, _ = _run_agent(
        monkeypatch,
        [
            AIMessage(content="", tool_calls=[{"name": "route_research", "args": {"destination": "香山"}, "id": "call-1"}]),
            AIMessage(content="推荐香山公园经典线，出发前核验天气。"),
        ],
        tools={"route_research": "香山公园经典线，成熟路线，推荐星级 4.5/5"},
        message="推荐一条香山徒步路线",
    )

    assert any(event["type"] == "tool_call" and event["metadata"]["tool"] == "route_research" for event in events)
    assert events[-1]["metadata"]["reason"] == "openmanus_completed"


def test_missing_params_no_longer_routes_to_clarification_lane(monkeypatch):
    events, _ = _run_agent(monkeypatch, [AIMessage(content="请补充目的地，我再继续规划。")], message="帮我规划路线")

    done = events[-1]
    text = "".join(event["content"] for event in events if event["type"] == "text")

    assert done["metadata"]["lane"] == "react"
    assert done["metadata"]["runtime"] == "openmanus"
    assert "目的地" in text


def test_high_risk_action_is_blocked_by_confirmation_event(monkeypatch):
    events, _ = _run_agent(
        monkeypatch,
        [
            AIMessage(content="", tool_calls=[{"name": "terminal", "args": {"command": "ls"}, "id": "call-1"}]),
            AIMessage(content="等待确认。"),
        ],
        tools={"terminal": "should not execute"},
        message="帮我运行 ls",
    )

    approval = next(event for event in events if event["type"] == "approval_required")

    assert approval["metadata"]["runtime"] == "openmanus"
    assert approval["metadata"]["tool"] == "terminal"
    assert approval["metadata"]["risk_level"] == "critical"
