import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from config import settings
from main import app


def collect_async(async_iterable):
    async def _collect():
        return [event async for event in async_iterable]

    return asyncio.run(_collect())


class FakeStreamingAgent:
    def __init__(self, updates):
        self.updates = updates
        self.calls = []

    async def astream(self, payload, **kwargs):
        self.calls.append((payload, kwargs))
        for update in self.updates:
            yield update


class FakeFailingStreamingAgent:
    def __init__(self, exc):
        self.exc = exc
        self.calls = []

    async def astream(self, payload, **kwargs):
        self.calls.append((payload, kwargs))
        raise self.exc
        yield


class FakeFailingInvokeAgent:
    def __init__(self, exc):
        self.exc = exc

    async def ainvoke(self, payload, **kwargs):
        raise self.exc


def test_agent_stream_routes_search_requests_through_langgraph(monkeypatch):
    """Search-like prompts should not bypass the unified LangGraph ReAct flow."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    fake_agent = FakeStreamingAgent([
        {
            "agent": {
                "messages": [
                    SimpleNamespace(content="统一 LangGraph 回复", tool_calls=[])
                ]
            }
        }
    ])

    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent", return_value=fake_agent):
        from agent import agent as agent_module

        async def fail_if_called(*args, **kwargs):
            raise AssertionError("web_search shortcut should not be called directly")

        monkeypatch.setattr(agent_module, "web_search", SimpleNamespace(ainvoke=fail_if_called))

        ai_agent = agent_module.AIAgent()
        events = collect_async(ai_agent.aexecute_stream("搜索北京周边徒步路线"))

    assert fake_agent.calls, "LangGraph agent stream should be used"
    assert any(event["type"] == "text" and event["content"] == "统一 LangGraph 回复" for event in events)
    assert not any("根据搜索结果" in event.get("content", "") for event in events)


def test_agent_stream_exits_gracefully_when_step_budget_is_exhausted(monkeypatch):
    """A LangGraph step-budget failure should become a controlled Agent exit, not raw model/runtime text."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    fake_agent = FakeFailingStreamingAgent(RuntimeError("Sorry, need more steps to process this request."))

    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent", return_value=fake_agent):
        from agent.agent import AIAgent

        ai_agent = AIAgent()
        events = collect_async(ai_agent.aexecute_stream("今天的天气适合去徒步吗"))

    text_events = [event for event in events if event["type"] == "text"]
    done_event = events[-1]

    assert text_events
    assert "Sorry, need more steps" not in text_events[-1]["content"]
    assert "执行步数上限" in text_events[-1]["content"]
    assert done_event["type"] == "done"
    assert done_event["metadata"]["status"] == "budget_exhausted"


def test_agent_sync_execute_exits_gracefully_when_step_budget_is_exhausted(monkeypatch):
    """The non-SSE Agent path should use the same controlled exit semantics."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    fake_agent = FakeFailingInvokeAgent(RuntimeError("Sorry, need more steps to process this request."))

    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent", return_value=fake_agent):
        from agent.agent import AIAgent

        result = asyncio.run(AIAgent().aexecute("帮我规划一个复杂徒步任务"))

    assert result["exit_status"] == "budget_exhausted"
    assert "Sorry, need more steps" not in result["output"]
    assert "执行步数上限" in result["output"]


def test_agent_stream_emits_react_tool_chain_details(monkeypatch):
    """Streaming should expose medium-grain ReAct steps: thought, tool call, result, final text."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    fake_agent = FakeStreamingAgent([
        {
            "agent": {
                "messages": [
                    SimpleNamespace(
                        content="",
                        tool_calls=[
                            {
                                "name": "web_search",
                                "args": {"query": "北京 徒步"},
                                "id": "call-1",
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
                        content="找到 3 条路线",
                        name="web_search",
                        tool_call_id="call-1",
                    )
                ]
            }
        },
        {
            "agent": {
                "messages": [
                    SimpleNamespace(content="推荐灵山和百花山。", tool_calls=[])
                ]
            }
        },
    ])

    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent", return_value=fake_agent):
        from agent.agent import AIAgent

        ai_agent = AIAgent()
        events = collect_async(ai_agent.aexecute_stream("帮我推荐北京周边徒步路线"))

    event_types = [event["type"] for event in events]
    assert "thought" in event_types
    assert "tool_call" in event_types
    assert "tool_result" in event_types
    assert "text" in event_types
    assert event_types[-1] == "done"

    tool_call = next(event for event in events if event["type"] == "tool_call")
    assert tool_call["metadata"]["step"] == 1
    assert tool_call["metadata"]["tool"] == "web_search"
    assert "北京" in tool_call["metadata"]["args"]

    tool_result = next(event for event in events if event["type"] == "tool_result")
    assert tool_result["metadata"]["step"] == 1
    assert tool_result["metadata"]["tool"] == "web_search"
    assert "找到 3 条路线" in tool_result["content"]


def test_agent_stream_stops_when_terminate_tool_returns(monkeypatch):
    """The terminate tool should act as a real task exit instead of a normal observation."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    fake_agent = FakeStreamingAgent([
        {
            "agent": {
                "messages": [
                    SimpleNamespace(
                        content="",
                        tool_calls=[
                            {
                                "name": "terminate",
                                "args": {"reason": "已经完成天气判断"},
                                "id": "call-stop-1",
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
                        content="任务已被 Agent 终止（原因: 已经完成天气判断）",
                        name="terminate",
                        tool_call_id="call-stop-1",
                    )
                ]
            }
        },
        {
            "agent": {
                "messages": [
                    SimpleNamespace(content="不应该继续生成这段文本", tool_calls=[])
                ]
            }
        },
    ])

    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent", return_value=fake_agent):
        from agent.agent import AIAgent

        ai_agent = AIAgent()
        events = collect_async(ai_agent.aexecute_stream("今天的天气适合去徒步吗"))

    final_text = "".join(event["content"] for event in events if event["type"] == "text")
    done_event = events[-1]

    assert "任务已结束：已经完成天气判断" in final_text
    assert "不应该继续生成" not in final_text
    assert done_event["type"] == "done"
    assert done_event["metadata"]["status"] == "completed"
    assert done_event["metadata"]["tool"] == "terminate"


def test_agent_prompt_contains_current_location_guidance(monkeypatch):
    """Location-aware prompts should tell the model how to turn browser coordinates into weather evidence."""
    monkeypatch.setattr(settings, "memory_enabled", False)

    with patch("agent.agent.ChatOpenAI"):
        from agent.agent import AIAgent, select_tools_for_context
        from agent.intake import understand_request

        ai_agent = AIAgent()
        context = understand_request(
            "今天的天气适合去徒步吗",
            current_location={"latitude": 39.9042, "longitude": 116.4074},
        )
        prompt = ai_agent._build_system_prompt(context, select_tools_for_context(context))

    assert "当前定位" in prompt
    assert "39.9042" in prompt
    assert "geo_lookup" in prompt
    assert "weather_lookup" in prompt


def test_agent_prompt_uses_structured_system_template(monkeypatch):
    """System prompt should follow the explicit Role/Goal/Constraints/Tools/Format/Examples template."""
    monkeypatch.setattr(settings, "memory_enabled", False)

    with patch("agent.agent.ChatOpenAI"):
        from agent.agent import AIAgent, select_tools_for_context
        from agent.intake import understand_request

        ai_agent = AIAgent()
        context = understand_request("今天的天气适合去徒步吗")
        prompt = ai_agent._build_system_prompt(context, select_tools_for_context(context))

    expected_tags = [
        "<Role>",
        "</Role>",
        "<Goal>",
        "</Goal>",
        "<Constraints>",
        "</Constraints>",
        "<Tools>",
        "</Tools>",
        "<Format>",
        "</Format>",
        "<Examples>",
        "</Examples>",
        "<RuntimeContext>",
        "</RuntimeContext>",
        "<NextStep>",
        "</NextStep>",
    ]
    for tag in expected_tags:
        assert tag in prompt
    assert "## 执行链路" not in prompt
    assert "## 本轮任务理解" not in prompt


def test_agent_stream_prefetches_current_location_weather_before_final_answer(monkeypatch):
    """Current-location weather questions should deterministically call geo and weather tools."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    tool_calls = []

    async def fake_geo_ainvoke(payload):
        tool_calls.append(("geo_lookup", payload))
        return {
            "ok": True,
            "source": "amap_regeo",
            "primary": {
                "city": "北京市",
                "district": "东城区",
                "adcode": "110101",
            },
        }

    async def fake_weather_ainvoke(payload):
        tool_calls.append(("weather_lookup", payload))
        return {
            "ok": True,
            "city": "东城区",
            "adcode": "110101",
            "weather": "晴",
            "temperature": "23°C",
            "wind_power": "3",
            "humidity": "40%",
            "report_time": "2026-05-19 16:00:00",
        }

    class FakeLLM:
        def invoke(self, messages):
            system = getattr(messages[0], "content", "")
            if "中文问题改写编辑" in system:
                return SimpleNamespace(content="今天的天气适合去徒步吗")
            return SimpleNamespace(
                content="结论：今天适合轻量徒步。天气晴，温度 23°C，风力 3 级，适合选择成熟短线。要不要我继续给你推荐附近的户外徒步路线？"
            )

    with patch("agent.agent.ChatOpenAI", return_value=FakeLLM()), patch("agent.agent.create_react_agent") as create_react_agent_mock:
        from agent import agent as agent_module
        from agent.agent import AIAgent

        monkeypatch.setattr(agent_module, "geo_lookup", SimpleNamespace(ainvoke=fake_geo_ainvoke, name="geo_lookup"))
        monkeypatch.setattr(agent_module, "weather_lookup", SimpleNamespace(ainvoke=fake_weather_ainvoke, name="weather_lookup"))

        ai_agent = AIAgent()
        events = collect_async(
            ai_agent.aexecute_stream(
                "今天的天气适合去徒步吗",
                current_location={"latitude": 39.9042, "longitude": 116.4074},
            )
        )

    assert [name for name, _ in tool_calls] == ["geo_lookup", "weather_lookup"]
    assert tool_calls[0][1]["latitude"] == 39.9042
    assert tool_calls[1][1]["adcode"] == "110101"
    assert create_react_agent_mock.called is False
    assert any(event["type"] == "tool_call" and event["metadata"]["tool"] == "geo_lookup" for event in events)
    assert any(event["type"] == "tool_call" and event["metadata"]["tool"] == "weather_lookup" for event in events)

    final_text = "".join(event["content"] for event in events if event["type"] == "text")
    assert "**" not in final_text
    assert not final_text.lstrip().startswith("1.")
    assert "适合轻量徒步" in final_text
    assert "要不要我继续给你推荐附近的户外徒步路线" in final_text
    assert events[-1]["type"] == "done"
    assert events[-1]["metadata"]["status"] == "completed"


def test_agent_stream_route_followup_researches_nearby_routes_with_ratings(monkeypatch):
    """When the user accepts route recommendations after a weather answer, Agent should research nearby routes directly."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    tool_calls = []

    async def fake_geo_ainvoke(payload):
        tool_calls.append(("geo_lookup", payload))
        return {
            "ok": True,
            "primary": {
                "city": "广州市",
                "district": "白云区",
                "adcode": "440111",
            },
        }

    async def fake_route_ainvoke(payload):
        tool_calls.append(("route_research", payload))
        return {
            "ok": True,
            "destination": "白云区",
            "search_results": [
                {
                    "query": "白云区 徒步 路线 推荐 星级",
                    "result": "白云山风景区徒步路线热度高；六片山路线适合短途徒步。",
                }
            ],
            "recommended_routes": [
                {"name": "白云山风景区徒步线", "rating": "4.6/5", "reason": "成熟路线，交通方便。"},
                {"name": "六片山短线", "rating": "4.2/5", "reason": "短途入门，强度较低。"},
            ],
        }

    class FakeLLM:
        def invoke(self, messages):
            system = getattr(messages[0], "content", "")
            if "中文问题改写编辑" in system:
                return SimpleNamespace(content="需要推荐附近徒步路线")
            return SimpleNamespace(
                content="我按白云区附近先搜了路线。白云山风景区徒步线，推荐星级 4.6/5，成熟路线，交通方便。六片山短线，推荐星级 4.2/5，适合短途入门。出发前再核验开放状态和天气。"
            )

    history = [
        {
            "role": "assistant",
            "content": "结论：今天适合轻量徒步。要不要我继续给你推荐附近的户外徒步路线？",
        }
    ]

    with patch("agent.agent.ChatOpenAI", return_value=FakeLLM()), patch("agent.agent.create_react_agent") as create_react_agent_mock:
        from agent import agent as agent_module
        from agent.agent import AIAgent

        monkeypatch.setattr(agent_module, "geo_lookup", SimpleNamespace(ainvoke=fake_geo_ainvoke, name="geo_lookup"))
        monkeypatch.setattr(agent_module, "route_research", SimpleNamespace(ainvoke=fake_route_ainvoke, name="route_research"))

        events = collect_async(
            AIAgent().aexecute_stream(
                "需要",
                history=history,
                current_location={"latitude": 23.1356, "longitude": 113.3441},
            )
        )

    assert [name for name, _ in tool_calls] == ["geo_lookup", "route_research"]
    assert tool_calls[1][1]["destination"] == "白云区"
    assert "推荐 星级" in tool_calls[1][1]["focus"]
    assert create_react_agent_mock.called is False
    assert any(event["type"] == "tool_call" and event["metadata"]["tool"] == "route_research" for event in events)

    final_text = "".join(event["content"] for event in events if event["type"] == "text")
    assert "推荐星级 4.6/5" in final_text
    assert "白云山" in final_text
    assert events[-1]["type"] == "done"
    assert events[-1]["metadata"]["status"] == "completed"


def test_agent_stream_uses_llm_query_rewrite_metadata(monkeypatch):
    """The stream should expose the LLM-rewritten query used for answer generation."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    fake_agent = FakeStreamingAgent([
        {
            "agent": {
                "messages": [
                    SimpleNamespace(content="可以，先看实时天气和路线风险。", tool_calls=[])
                ]
            }
        }
    ])

    class FakeLLM:
        def invoke(self, messages):
            return SimpleNamespace(content="今天本地天气适合徒步吗")

    with patch("agent.agent.ChatOpenAI", return_value=FakeLLM()), patch("agent.agent.create_react_agent", return_value=fake_agent):
        from agent.agent import AIAgent

        ai_agent = AIAgent()
        events = collect_async(ai_agent.aexecute_stream("今天的天气适合去徒步吗"))

    rewrite_event = next(
        event for event in events
        if event["type"] == "thought" and event.get("metadata", {}).get("phase") == "query_rewrite"
    )
    assert rewrite_event["metadata"]["rewritten_query"] == "今天本地天气适合徒步吗"


def test_agent_stream_emits_approval_required_for_high_risk_tool(monkeypatch):
    """High-risk tool calls should surface approval before the tool result is accepted."""
    monkeypatch.setattr(settings, "memory_enabled", False)
    fake_agent = FakeStreamingAgent([
        {
            "agent": {
                "messages": [
                    SimpleNamespace(
                        content="",
                        tool_calls=[
                            {
                                "name": "file_operation",
                                "args": {"operation": "write", "path": "plan.md", "content": "x"},
                                "id": "call-approval-1",
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
                        content="文件已写入: plan.md",
                        name="file_operation",
                        tool_call_id="call-approval-1",
                    )
                ]
            }
        },
    ])

    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent", return_value=fake_agent):
        from agent.agent import AIAgent

        ai_agent = AIAgent()
        events = collect_async(ai_agent.aexecute_stream("写入徒步计划"))

    approval = next(event for event in events if event["type"] == "approval_required")
    assert approval["metadata"]["tool"] == "file_operation"
    assert approval["metadata"]["risk_level"] == "high"
    assert approval["metadata"]["tool_call_id"] == "call-approval-1"

    tool_results = [event for event in events if event["type"] == "tool_result"]
    assert not any("文件已写入" in event["content"] for event in tool_results)


def test_chat_sse_persists_assistant_reply_and_emits_single_done(monkeypatch):
    """SSE endpoint should persist final assistant text once the stream completes."""
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    stored_messages = []

    class FakeMemory:
        def __init__(self, chat_id):
            self.chat_id = chat_id

        def add_message(self, role, content):
            stored_messages.append({"role": role, "content": content})

        def get_messages(self):
            return stored_messages.copy()

    class FakeAgent:
        def __init__(self, *args, **kwargs):
            pass

        async def aexecute_stream(self, message, history=None):
            yield {"type": "thought", "content": "第 1 步：分析需求"}
            yield {"type": "text", "content": "第一段"}
            yield {"type": "text", "content": "第二段"}
            yield {"type": "done", "content": ""}

    from api import chat as chat_api

    monkeypatch.setattr(chat_api, "_get_memory", lambda chat_id: FakeMemory(chat_id))
    monkeypatch.setattr(chat_api, "AIAgent", FakeAgent)

    client = TestClient(app)
    response = client.post(
        "/api/v1/chat/sse",
        json={"chat_id": "agent-flow-test", "message": "制定徒步计划"},
    )

    assert response.status_code == 200
    events = []
    for line in response.iter_lines():
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        if line.startswith("data: "):
            events.append(json.loads(line[6:]))

    assert [msg["role"] for msg in stored_messages] == ["user", "assistant"]
    assert stored_messages[1]["content"] == "第一段第二段"
    assert sum(1 for event in events if event["type"] == "done") == 1


def test_chat_sse_passes_current_location_to_agent(monkeypatch):
    """SSE endpoint should preserve browser location for Agent tool planning."""
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    received = {}

    class FakeMemory:
        def __init__(self, chat_id):
            self.messages = []

        def add_message(self, role, content):
            self.messages.append({"role": role, "content": content})

        def get_messages(self):
            return self.messages.copy()

    class FakeAgent:
        def __init__(self, *args, **kwargs):
            pass

        async def aexecute_stream(self, message, history=None, **kwargs):
            received.update(kwargs)
            yield {"type": "text", "content": "ok"}
            yield {"type": "done", "content": ""}

    from api import chat as chat_api

    monkeypatch.setattr(chat_api, "_get_memory", lambda chat_id: FakeMemory(chat_id))
    monkeypatch.setattr(chat_api, "AIAgent", FakeAgent)

    client = TestClient(app)
    response = client.post(
        "/api/v1/chat/sse",
        json={
            "chat_id": "agent-location-test",
            "message": "今天的天气适合去徒步吗",
            "current_location": {
                "latitude": 39.9042,
                "longitude": 116.4074,
                "accuracy": 30,
                "source": "browser",
            },
        },
    )

    assert response.status_code == 200
    assert received["current_location"]["latitude"] == 39.9042
    assert received["current_location"]["longitude"] == 116.4074
