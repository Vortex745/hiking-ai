"""单元测试：AIAgent 工具注册表与 tool_call 风险元数据。

覆盖范围：
  - AIAgent.get_tool_registry() 静态方法返回正确的注册表实例
  - 已知工具的 risk_level / needs_confirmation / rate_limit_exceeded
  - 未知工具的回退行为
  - 速率限制耗尽检测
  - 单例身份验证
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.tool_registry import ToolRegistry


# ─── 辅助工具 ────────────────────────────────────────────


class FakeStreamingAgent:
    """模拟 LangGraph ReAct agent 的流式迭代输出。"""

    def __init__(self, updates):
        self.updates = updates
        self.calls = []

    async def astream(self, payload, **kwargs):
        self.calls.append((payload, kwargs))
        for update in self.updates:
            yield update


def collect_async(async_iterable):
    """同步消费异步生成器，返回全部事件的列表。"""
    import asyncio

    async def _collect():
        return [event async for event in async_iterable]

    return asyncio.run(_collect())


def _make_tool_call_update(tool_name: str, args: dict, call_id: str = "call-1"):
    """构建一个包含单次工具调用的流更新序列。"""
    return [
        {
            "agent": {
                "messages": [
                    SimpleNamespace(
                        content="",
                        tool_calls=[
                            {
                                "name": tool_name,
                                "args": args,
                                "id": call_id,
                            }
                        ],
                    )
                ]
            }
        },
        {
            "tools": {
                "messages": [
                    SimpleNamespace(
                        content="输出占位",
                        name=tool_name,
                        tool_call_id=call_id,
                    )
                ]
            }
        },
        {
            "agent": {
                "messages": [
                    SimpleNamespace(content="任务完成", tool_calls=[])
                ]
            }
        },
    ]


# ─── Test: get_tool_registry ─────────────────────────────


def test_get_tool_registry_returns_tool_registry_instance():
    """get_tool_registry() 应返回一个 ToolRegistry 实例。"""
    from agent.agent import AIAgent

    registry = AIAgent.get_tool_registry()
    assert isinstance(registry, ToolRegistry)


def test_get_tool_registry_has_expected_tools():
    """get_tool_registry() 返回的注册表应包含所有定义的 AVAILABLE_TOOLS。"""
    from agent.agent import AIAgent

    registry = AIAgent.get_tool_registry()
    expected_tools = {
        "web_search",
        "web_scraping",
        "file_operation",
        "resource_download",
        "terminal",
        "generate_pdf",
        "terminate",
    }
    registered_names = {md.name for md in registry.list_tools()}
    assert registered_names == expected_tools, (
        f"缺失工具: {expected_tools - registered_names}"
    )


def test_get_tool_registry_is_singleton():
    """get_tool_registry() 多次调用应返回同一个注册表实例（模块级单例）。"""
    from agent.agent import AIAgent, tool_registry

    assert AIAgent.get_tool_registry() is tool_registry


# ─── Test: tool_call metadata 富化 ────────────────────────


def test_tool_call_metadata_has_risk_fields(monkeypatch):
    """tool_call 事件的 metadata 应包含 risk_level / needs_confirmation / rate_limit_exceeded。"""
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)

    fake = FakeStreamingAgent(
        _make_tool_call_update("web_search", {"query": "test"}, "call-1")
    )

    with patch("agent.agent.ChatOpenAI"), patch(
        "agent.agent.create_react_agent", return_value=fake
    ):
        from agent.agent import AIAgent

        agent = AIAgent()
        events = collect_async(agent.aexecute_stream("test"))

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]
    assert "risk_level" in meta
    assert "needs_confirmation" in meta
    assert "rate_limit_exceeded" in meta
    assert isinstance(meta["risk_level"], str)
    assert isinstance(meta["needs_confirmation"], bool)
    assert isinstance(meta["rate_limit_exceeded"], bool)


def test_low_risk_tool_metadata(monkeypatch):
    """web_search (LOW) 的 tool_call metadata。"""
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)

    fake = FakeStreamingAgent(
        _make_tool_call_update("web_search", {"query": "hiking"}, "call-1")
    )

    with patch("agent.agent.ChatOpenAI"), patch(
        "agent.agent.create_react_agent", return_value=fake
    ):
        from agent.agent import AIAgent

        agent = AIAgent()
        events = collect_async(agent.aexecute_stream("test"))

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]
    assert meta["risk_level"] == "low"
    assert meta["needs_confirmation"] is False
    assert meta["rate_limit_exceeded"] is False


def test_medium_risk_tool_metadata(monkeypatch):
    """web_scraping (MEDIUM) 的 tool_call metadata。"""
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)

    fake = FakeStreamingAgent(
        _make_tool_call_update("web_scraping", {"url": "http://example.com"}, "call-1")
    )

    with patch("agent.agent.ChatOpenAI"), patch(
        "agent.agent.create_react_agent", return_value=fake
    ):
        from agent.agent import AIAgent

        agent = AIAgent()
        events = collect_async(agent.aexecute_stream("test"))

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]
    assert meta["risk_level"] == "medium"
    assert meta["needs_confirmation"] is False
    assert meta["rate_limit_exceeded"] is False


def test_high_risk_tool_metadata(monkeypatch):
    """file_operation (HIGH) 的 tool_call metadata → needs_confirmation=True。"""
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)

    fake = FakeStreamingAgent(
        _make_tool_call_update(
            "file_operation",
            {"operation": "create", "path": "/tmp/test"},
            "call-1",
        )
    )

    with patch("agent.agent.ChatOpenAI"), patch(
        "agent.agent.create_react_agent", return_value=fake
    ):
        from agent.agent import AIAgent

        agent = AIAgent()
        events = collect_async(agent.aexecute_stream("test"))

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]
    assert meta["risk_level"] == "high"
    assert meta["needs_confirmation"] is True
    assert meta["rate_limit_exceeded"] is False


def test_critical_risk_tool_metadata(monkeypatch):
    """terminal (CRITICAL) 的 tool_call metadata。"""
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)

    fake = FakeStreamingAgent(
        _make_tool_call_update("terminal", {"command": "ls"}, "call-1")
    )

    with patch("agent.agent.ChatOpenAI"), patch(
        "agent.agent.create_react_agent", return_value=fake
    ):
        from agent.agent import AIAgent

        agent = AIAgent()
        events = collect_async(agent.aexecute_stream("test"))

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]
    assert meta["risk_level"] == "critical"
    assert meta["needs_confirmation"] is True
    assert meta["rate_limit_exceeded"] is False


def test_unknown_tool_falls_back_to_medium_risk(monkeypatch):
    """未注册工具应回退为 MEDIUM 风险、无需确认、无速率限制。"""
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)

    fake = FakeStreamingAgent(
        _make_tool_call_update("unknown_tool", {}, "call-1")
    )

    with patch("agent.agent.ChatOpenAI"), patch(
        "agent.agent.create_react_agent", return_value=fake
    ):
        from agent.agent import AIAgent

        agent = AIAgent()
        events = collect_async(agent.aexecute_stream("test"))

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]
    assert meta["risk_level"] == "medium"
    assert meta["needs_confirmation"] is False
    assert meta["rate_limit_exceeded"] is False


def test_rate_limited_tool_detection(monkeypatch):
    """速率限制耗尽时 rate_limit_exceeded 应为 True。"""
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)

    from agent.agent import tool_registry

    # 将 terminal 的令牌桶耗尽
    bucket = tool_registry._buckets["terminal"]
    bucket.tokens = 0.0

    fake = FakeStreamingAgent(
        _make_tool_call_update("terminal", {"command": "ls"}, "call-1")
    )

    with patch("agent.agent.ChatOpenAI"), patch(
        "agent.agent.create_react_agent", return_value=fake
    ):
        from agent.agent import AIAgent

        agent = AIAgent()
        events = collect_async(agent.aexecute_stream("test"))

    tool_call = next(e for e in events if e["type"] == "tool_call")
    meta = tool_call["metadata"]
    assert meta["rate_limit_exceeded"] is True
    # 风险字段应不受影响
    assert meta["risk_level"] == "critical"
    assert meta["needs_confirmation"] is True
