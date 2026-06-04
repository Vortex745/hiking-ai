"""OpenManus-only Agent execution flow tests."""

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
        return self

    def invoke(self, messages):
        if self.responses:
            response = self.responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return response
        return AIMessage(content="任务已完成。")


def _fake_tool(name: str, result: str = "ok"):
    if isinstance(result, list):
        runner = AsyncMock(side_effect=result)
    else:
        runner = AsyncMock(return_value=result)
    return SimpleNamespace(
        name=name,
        description=f"{name} fake tool",
        ainvoke=runner,
    )


def _run(monkeypatch, responses, *, tools=None, message="帮我推荐北京周边徒步路线"):
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    fake_llm = FakeToolModel(responses)

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent import agent as agent_module
        from agent.agent import AIAgent

        has_legacy_langgraph_entrypoint = hasattr(agent_module, "create_react_agent")
        for tool_name, result in (tools or {"web_search": "找到 3 条路线"}).items():
            fake_tool = _fake_tool(tool_name, result)
            monkeypatch.setitem(agent_module.AVAILABLE_TOOL_MAP, tool_name, fake_tool)
            monkeypatch.setattr(agent_module, tool_name, fake_tool, raising=False)

        events = collect_async(AIAgent().aexecute_stream(message))

    return events, has_legacy_langgraph_entrypoint, fake_llm


def test_agent_stream_uses_openmanus_not_langgraph(monkeypatch):
    events, has_legacy_langgraph_entrypoint, fake_llm = _run(
        monkeypatch,
        [AIMessage(content="统一 OpenManus 回复")],
        message="搜索北京周边徒步路线",
    )

    assert has_legacy_langgraph_entrypoint is False
    assert fake_llm.bound_tools
    assert events[0]["metadata"]["runtime"] == "openmanus"
    assert events[-1]["metadata"]["reason"] == "openmanus_completed"


def test_agent_final_answer_bolds_route_metrics_and_risk_terms(monkeypatch):
    events, _, _ = _run(
        monkeypatch,
        [AIMessage(content="白云山南门全程8-10公里，门票5元，高温时不建议正午出发。")],
        message="白云山徒步路线怎么走",
    )

    final_text = "".join(event["content"] for event in events if event["type"] == "text")

    assert "**白云山南门**" in final_text
    assert "**8-10公里**" in final_text
    assert "**5元**" in final_text
    assert "**高温**" in final_text
    assert "**不建议**" in final_text


def test_agent_stream_emits_openmanus_tool_chain_details(monkeypatch):
    events, _, _ = _run(
        monkeypatch,
        [
            AIMessage(content="", tool_calls=[{"name": "web_search", "args": {"query": "北京 徒步"}, "id": "call-1"}]),
            AIMessage(content="推荐灵山和百花山。"),
        ],
    )

    event_types = [event["type"] for event in events]
    assert "thought" in event_types
    assert "tool_call" in event_types
    assert "tool_result" in event_types
    assert "text" in event_types
    assert events[-1]["type"] == "done"

    tool_call = next(event for event in events if event["type"] == "tool_call")
    assert tool_call["metadata"]["runtime"] == "openmanus"
    assert tool_call["metadata"]["step"] == 1
    assert tool_call["metadata"]["tool"] == "web_search"


def test_agent_stream_emits_artifact_event_for_generated_pdf(monkeypatch):
    pdf_output = {
        "ok": True,
        "message": "PDF 已生成：plan.pdf",
        "artifact": {
            "kind": "pdf",
            "title": "Trip plan",
            "filename": "plan.pdf",
            "relative_path": "plan.pdf",
            "download_url": "/api/v1/artifacts/plan.pdf",
            "mime_type": "application/pdf",
            "size_bytes": 2048,
        },
    }
    events, _, _ = _run(
        monkeypatch,
        [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "generate_pdf",
                        "args": {"title": "Trip plan", "content": "Safe route"},
                        "id": "call-pdf-1",
                    }
                ],
            ),
            AIMessage(content="已生成，可在下方下载。"),
        ],
        tools={"generate_pdf": pdf_output},
        message="请把这份徒步计划导出 PDF",
    )

    artifact = next(event for event in events if event["type"] == "artifact")

    assert artifact["content"] == "PDF 已生成：plan.pdf"
    assert artifact["metadata"]["filename"] == "plan.pdf"
    assert artifact["metadata"]["download_url"] == "/api/v1/artifacts/plan.pdf"
    assert artifact["metadata"]["mime_type"] == "application/pdf"


def test_complex_route_plan_binds_domain_tools_without_generic_search(monkeypatch):
    events, _, fake_llm = _run(
        monkeypatch,
        [AIMessage(content="已生成广州一日徒步计划。")],
        message="帮我规划一个从广州出发的一日徒步路线，需要查看天气、推荐路线、检查装备清单和评估风险",
    )

    bound_names = {tool.name for tool in fake_llm.bound_tools}

    assert events[-1]["metadata"]["reason"] == "openmanus_completed"
    assert {"weather_lookup", "route_research", "gear_checklist", "risk_assessment", "terminate"}.issubset(bound_names)
    assert "web_search" not in bound_names
    assert "web_scraping" not in bound_names


def test_agent_stream_stops_when_terminate_tool_returns(monkeypatch):
    events, _, _ = _run(
        monkeypatch,
        [
            AIMessage(content="", tool_calls=[{"name": "terminate", "args": {"reason": "已经完成天气判断"}, "id": "call-stop-1"}]),
            AIMessage(content="不应该继续生成这段文本"),
        ],
        tools={"terminate": "任务已被 Agent 终止（原因: 已经完成天气判断）"},
        message="帮我分析一下徒步的注意事项",
    )

    final_text = "".join(event["content"] for event in events if event["type"] == "text")
    done_event = events[-1]

    assert "任务已结束：已经完成天气判断" in final_text
    assert "不应该继续" not in final_text
    assert done_event["metadata"]["tool"] == "terminate"


def test_agent_stream_emits_approval_required_for_high_risk_tool(monkeypatch):
    events, _, _ = _run(
        monkeypatch,
        [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "file_operation",
                        "args": {"operation": "create", "path": "/tmp/demo"},
                        "id": "call-approval-1",
                    }
                ],
            ),
            AIMessage(content="需要确认。"),
        ],
        tools={"file_operation": "should not run"},
    )

    approval = next(event for event in events if event["type"] == "approval_required")

    assert approval["metadata"]["tool"] == "file_operation"
    assert approval["metadata"]["tool_call_id"] == "call-approval-1"
    assert approval["metadata"]["needs_confirmation"] is True


def test_agent_stream_repeat_call_guard_skips_duplicate_calls(monkeypatch):
    events, _, _ = _run(
        monkeypatch,
        [
            AIMessage(content="", tool_calls=[{"name": "weather_lookup", "args": {"adcode": "110101"}, "id": "call-1"}]),
            AIMessage(content="", tool_calls=[{"name": "weather_lookup", "args": {"adcode": "110101"}, "id": "call-2"}]),
        ],
        tools={"weather_lookup": "晴，23°C"},
        message="查询天气",
    )

    weather_calls = [
        event
        for event in events
        if event["type"] == "tool_call" and event["metadata"]["tool"] == "weather_lookup"
    ]

    assert len(weather_calls) == 1
    assert events[-1]["metadata"]["status"] == "stuck"


def test_agent_stream_gracefully_handles_step_budget(monkeypatch):
    responses = [
        AIMessage(content="", tool_calls=[{"name": "web_search", "args": {"query": f"路线 {idx}"}, "id": f"call-{idx}"}])
        for idx in range(10)
    ]
    events, _, _ = _run(
        monkeypatch,
        responses,
        tools={"web_search": [f"找到路线 {idx}" for idx in range(10)]},
        message="帮我搜索一些户外资料",
    )

    text_events = [event for event in events if event["type"] == "text"]
    done_event = events[-1]

    assert text_events
    assert "执行步数上限" in text_events[-1]["content"]
    assert done_event["metadata"]["status"] == "budget_exhausted"


def test_agent_sync_execute_uses_openmanus_path(monkeypatch):
    monkeypatch.setattr("agent.agent.settings.memory_enabled", False)
    fake_llm = FakeToolModel([AIMessage(content="同步 OpenManus 回复")])

    with patch("agent.agent.ChatOpenAI", return_value=fake_llm):
        from agent.agent import AIAgent

        result = asyncio.run(AIAgent().aexecute("你好"))

    assert result["output"] == "同步 OpenManus 回复"
    assert result["metadata"]["runtime"] == "openmanus"
    assert result["metadata"]["reason"] == "openmanus_completed"
