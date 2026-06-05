"""Observability tests for OpenManus-only Agent execution."""

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


def _fake_tool(name: str, result: str = "ok"):
    return SimpleNamespace(
        name=name,
        description=f"{name} fake tool",
        ainvoke=AsyncMock(return_value=result),
    )


def _run_openmanus(monkeypatch, responses, *, tool_name="web_search"):
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    monkeypatch.setattr("agent.agent.settings.mcp_servers", {})
    fake_llm = FakeToolModel(responses)

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent import agent as agent_module
        from agent.agent import AIAgent

        fake_tool = _fake_tool(tool_name, f"{tool_name} result")
        monkeypatch.setitem(agent_module.AVAILABLE_TOOL_MAP, tool_name, fake_tool)
        monkeypatch.setattr(agent_module, tool_name, fake_tool, raising=False)

        return collect_async(AIAgent().aexecute_stream("帮我看看"))


def _assert_done_observability(done_event):
    meta = done_event["metadata"]
    assert meta["runtime"] == "openmanus"
    assert meta["lane"] == "react"
    assert "exit_reason" in meta
    assert isinstance(meta["step_count"], int)
    assert isinstance(meta["selected_tools"], list)
    assert isinstance(meta["duration_ms"], (int, float))
    assert meta["duration_ms"] > 0
    assert meta["openmanus_runtime"]["base"] == "BaseAgent"
    assert meta["openmanus_runtime"]["tool_call"] == "ToolCallAgent"


def test_openmanus_done_event_has_observability_fields(monkeypatch):
    events = _run_openmanus(monkeypatch, [AIMessage(content="你好，我是 AI Hiking。")])

    done = next(e for e in reversed(events) if e["type"] == "done")

    _assert_done_observability(done)
    assert done["metadata"]["status"] == "completed"


def test_openmanus_tool_call_has_step_and_tool(monkeypatch):
    events = _run_openmanus(
        monkeypatch,
        [
            AIMessage(content="", tool_calls=[{"name": "web_search", "args": {"query": "北京 徒步"}, "id": "call-1"}]),
            AIMessage(content="推荐灵山。"),
        ],
    )

    tool_call = next(e for e in events if e["type"] == "tool_call")
    tool_result = next(e for e in events if e["type"] == "tool_result")

    assert tool_call["metadata"]["step"] >= 1
    assert tool_call["metadata"]["tool"] == "web_search"
    assert tool_call["metadata"]["runtime"] == "openmanus"
    assert tool_result["metadata"]["tool"] == "web_search"


def test_openmanus_approval_event_has_observability_fields(monkeypatch):
    events = _run_openmanus(
        monkeypatch,
        [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "terminal",
                        "args": {"command": "ls"},
                        "id": "call-1",
                    }
                ],
            ),
            AIMessage(content="需要确认。"),
        ],
        tool_name="terminal",
    )

    approval = next(e for e in events if e["type"] == "approval_required")

    assert approval["metadata"]["runtime"] == "openmanus"
    assert approval["metadata"]["risk_level"] == "critical"
    assert approval["metadata"]["needs_confirmation"] is True
