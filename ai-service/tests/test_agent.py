"""Agent tests for the OpenManus-only execution path."""

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
        self.bound_tools = []

    def bind_tools(self, tools, tool_choice="auto"):
        self.bound_tools = tools
        self.tool_choice = tool_choice
        return self

    def invoke(self, messages):
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
    assert "weather_lookup" in names
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
