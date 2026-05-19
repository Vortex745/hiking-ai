import asyncio
import json
import logging
import re
from typing import Any, AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent.intake import AgentIntent, AgentRequestContext, CurrentLocation, understand_request
from agent.prompts import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from agent.task_exit import AgentTaskExitController
from api.models import RuntimeLlmConfig
from config import settings
from memory import MemoryManager
from rag.rewriter import QueryRewriter
from rag.text_processing import clean_display_text
from tools.file_operation import file_operation
from tools.hiking_domain import (
    gear_checklist,
    geo_lookup,
    risk_assessment,
    route_research,
    trip_report_export,
    weather_lookup,
)
from tools.hiking_knowledge import hiking_knowledge_search
from tools.pdf_generation import generate_pdf
from tools.resource_download import resource_download
from tools.risk_classifier import TOOL_RISK_MAP, RiskLevel
from tools.terminal import terminal
from tools.terminate import terminate
from tools.tool_registry import ToolMetadata, ToolRegistry
from tools.web_scraping import web_scraping
from tools.web_search import web_search

logger = logging.getLogger("ai-service.agent")

MAX_STEPS = 6
MAX_EVENT_CHARS = 1200
MAX_ARGS_CHARS = 500
ROUTE_RECOMMENDATION_PROMPT = "要不要我继续给你推荐附近的户外徒步路线？"
ROUTE_FOLLOWUP_MARKERS = (
    ROUTE_RECOMMENDATION_PROMPT,
    "要不要我继续给你推荐",
    "是否要推荐",
    "推荐附近的户外徒步路线",
)
AFFIRMATIVE_ROUTE_FOLLOWUP = (
    "需要",
    "要",
    "好的",
    "好",
    "可以",
    "行",
    "安排",
    "推荐",
    "继续",
)


BASE_TOOL_NAMES = [
    "web_search",
    "web_scraping",
    "file_operation",
    "resource_download",
    "terminal",
    "generate_pdf",
    "terminate",
]

AVAILABLE_TOOL_MAP = {
    "web_search": web_search,
    "web_scraping": web_scraping,
    "file_operation": file_operation,
    "resource_download": resource_download,
    "terminal": terminal,
    "generate_pdf": generate_pdf,
    "terminate": terminate,
    "weather_lookup": weather_lookup,
    "geo_lookup": geo_lookup,
    "route_research": route_research,
    "hiking_knowledge_search": hiking_knowledge_search,
    "gear_checklist": gear_checklist,
    "risk_assessment": risk_assessment,
    "trip_report_export": trip_report_export,
}

AVAILABLE_TOOLS = [AVAILABLE_TOOL_MAP[name] for name in BASE_TOOL_NAMES]

INTENT_TOOL_NAMES: dict[AgentIntent, list[str]] = {
    AgentIntent.KNOWLEDGE_QA: [
        "hiking_knowledge_search",
        "terminate",
    ],
    AgentIntent.ROUTE_PLAN: [
        "weather_lookup",
        "geo_lookup",
        "route_research",
        "hiking_knowledge_search",
        "gear_checklist",
        "risk_assessment",
        "terminate",
    ],
    AgentIntent.GEAR_CHECK: [
        "hiking_knowledge_search",
        "gear_checklist",
        "risk_assessment",
        "terminate",
    ],
    AgentIntent.RISK_ASSESSMENT: [
        "weather_lookup",
        "geo_lookup",
        "route_research",
        "hiking_knowledge_search",
        "risk_assessment",
        "terminate",
    ],
    AgentIntent.REPORT_EXPORT: [
        "route_research",
        "hiking_knowledge_search",
        "gear_checklist",
        "risk_assessment",
        "trip_report_export",
        "generate_pdf",
        "file_operation",
        "terminate",
    ],
    AgentIntent.GENERAL_CHAT: [
        "web_search",
        "web_scraping",
        "terminate",
    ],
}


def _unique_tool_names(names: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for name in names:
        if name not in seen and name in AVAILABLE_TOOL_MAP:
            seen.add(name)
            result.append(name)
    return result


def _prefetched_tool_names(context: AgentRequestContext) -> set[str]:
    names: set[str] = set()
    for item in context.prefetched_tool_results:
        tool = item.get("tool") if isinstance(item, dict) else None
        if tool:
            names.add(str(tool))
    return names


def select_tools_for_context(context: AgentRequestContext) -> list:
    """Return the small tool set visible to the model for one request."""
    if context.needs_clarification and context.intent in {
        AgentIntent.ROUTE_PLAN,
        AgentIntent.RISK_ASSESSMENT,
    }:
        tool_names = ["terminate"]
    elif context.intent == AgentIntent.GENERAL_CHAT:
        tool_names = ["terminate"]
    elif (
        context.intent == AgentIntent.RISK_ASSESSMENT
        and {"geo_lookup", "weather_lookup"}.issubset(_prefetched_tool_names(context))
    ):
        tool_names = ["risk_assessment", "terminate"]
    else:
        tool_names = INTENT_TOOL_NAMES.get(context.intent, INTENT_TOOL_NAMES[AgentIntent.GENERAL_CHAT])
    return [AVAILABLE_TOOL_MAP[name] for name in _unique_tool_names(tool_names)]


def validate_tool_configuration() -> dict[str, Any]:
    """Validate local tool implementation, registry, risk map, and intent routing."""
    available_names = set(AVAILABLE_TOOL_MAP)
    registered_names = {md.name for md in tool_registry.list_all_tools()}
    risk_names = set(TOOL_RISK_MAP)
    intent_names = {
        name
        for names in INTENT_TOOL_NAMES.values()
        for name in names
    }
    base_names = set(BASE_TOOL_NAMES)

    issues: list[dict[str, Any]] = []

    def add_issue(kind: str, names: set[str]) -> None:
        if names:
            issues.append({"kind": kind, "tools": sorted(names)})

    add_issue("available_not_registered", available_names - registered_names)
    add_issue("registered_not_available", registered_names - available_names)
    add_issue("available_missing_risk", available_names - risk_names)
    add_issue("intent_not_available", intent_names - available_names)
    add_issue("base_not_available", base_names - available_names)

    return {
        "ok": not issues,
        "issues": issues,
        "available_count": len(available_names),
        "registered_count": len(registered_names),
        "risk_count": len(risk_names & available_names),
        "intent_tool_count": len(intent_names),
        "base_tool_count": len(base_names),
    }


def _approval_required_payload(tool_name: str, args: dict[str, Any]) -> str:
    payload = {
        "type": "approval_required",
        "tool": tool_name,
        "args": args,
        "message": f"工具 {tool_name} 需要用户确认后才能执行。",
    }
    return json.dumps(payload, ensure_ascii=False)


def _guard_tool_for_confirmation(tool):
    md = tool_registry.get(tool.name)
    if md is None or not tool_registry.needs_confirmation(tool.name):
        return tool

    async def guarded_runner(**kwargs) -> str:
        return _approval_required_payload(tool.name, kwargs)

    return StructuredTool.from_function(
        name=tool.name,
        description=tool.description,
        args_schema=getattr(tool, "args_schema", None),
        coroutine=guarded_runner,
    )


def apply_tool_confirmation_guards(tools: list) -> list:
    """Wrap high-risk tools so the model cannot execute side effects before approval."""
    return [_guard_tool_for_confirmation(tool) for tool in tools]


tool_registry = ToolRegistry()
tool_registry.register_many([
    ToolMetadata(
        name="web_search",
        description="Search the web for information relevant to the user's query or task.",
        parameters={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=30,
        domain="web",
        scenarios=("general_chat", "route_plan"),
        result_policy="compact",
    ),
    ToolMetadata(
        name="web_scraping",
        description="Scrape and extract main content from a web page URL.",
        parameters={"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
        risk_level=RiskLevel.MEDIUM,
        rate_limit_per_minute=20,
        domain="web",
        scenarios=("general_chat", "route_plan"),
        result_policy="compact",
    ),
    ToolMetadata(
        name="file_operation",
        description="Create, read, update, delete, or list files/directories in the workspace.",
        parameters={
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["create", "read", "update", "delete", "list", "write", "mkdir"]},
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["operation", "path"],
        },
        risk_level=RiskLevel.HIGH,
        rate_limit_per_minute=20,
        domain="filesystem",
        scenarios=("report_export",),
        auto_allowed=False,
        result_policy="artifact",
    ),
    ToolMetadata(
        name="resource_download",
        description="Download a resource from a URL to local workspace.",
        parameters={
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "save_path": {"type": "string"},
            },
            "required": ["url"],
        },
        risk_level=RiskLevel.MEDIUM,
        rate_limit_per_minute=10,
        domain="filesystem",
        auto_allowed=False,
        result_policy="artifact",
    ),
    ToolMetadata(
        name="terminal",
        description="Execute a command in the local terminal/shell environment.",
        parameters={"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]},
        risk_level=RiskLevel.CRITICAL,
        rate_limit_per_minute=10,
        domain="system",
        auto_allowed=False,
        result_policy="raw",
    ),
    ToolMetadata(
        name="generate_pdf",
        description="Generate a PDF document from text content.",
        parameters={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["title", "content"],
        },
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=10,
        domain="artifact",
        scenarios=("report_export",),
        result_policy="artifact",
    ),
    ToolMetadata(
        name="terminate",
        description="Call this when the task is complete or cannot continue further.",
        parameters={"type": "object", "properties": {"reason": {"type": "string"}}},
        risk_level=RiskLevel.HIGH,
        needs_confirmation=False,
        rate_limit_per_minute=60,
        domain="control",
        result_policy="compact",
    ),
    ToolMetadata(
        name="weather_lookup",
        description="Look up hiking weather envelope for a destination and date.",
        parameters={
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "date": {"type": "string"},
                "adcode": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
            },
        },
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=20,
        domain="hiking",
        scenarios=("route_plan", "risk_assessment"),
        result_policy="compact",
        hidden=True,
    ),
    ToolMetadata(
        name="geo_lookup",
        description="Look up geolocation and terrain envelope for a hiking destination.",
        parameters={
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "latitude": {"type": "number"},
                "longitude": {"type": "number"},
            },
        },
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=20,
        domain="hiking",
        scenarios=("route_plan", "risk_assessment"),
        result_policy="compact",
        hidden=True,
    ),
    ToolMetadata(
        name="route_research",
        description="Collect hiking route facts from search queries, web reading, and RAG evidence.",
        parameters={
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "date": {"type": "string"},
                "days": {"type": "integer"},
                "focus": {"type": "string"},
            },
            "required": ["destination"],
        },
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=20,
        domain="hiking",
        scenarios=("route_plan", "risk_assessment", "report_export"),
        result_policy="compact",
        hidden=True,
    ),
    ToolMetadata(
        name="hiking_knowledge_search",
        description="Search the hiking RAG knowledge base and return traceable evidence chunks.",
        parameters={"type": "object", "properties": {"query": {"type": "string"}, "k": {"type": "integer"}}, "required": ["query"]},
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=30,
        domain="hiking",
        scenarios=("knowledge_qa", "route_plan", "gear_check", "risk_assessment", "report_export"),
        result_policy="compact",
        hidden=True,
    ),
    ToolMetadata(
        name="gear_checklist",
        description="Generate a conservative hiking gear checklist.",
        parameters={
            "type": "object",
            "properties": {
                "days": {"type": "integer"},
                "season": {"type": "string"},
                "experience": {"type": "string"},
                "camping": {"type": "boolean"},
                "gear_level": {"type": "string"},
            },
        },
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=30,
        domain="hiking",
        scenarios=("gear_check", "route_plan", "report_export"),
        result_policy="compact",
        hidden=True,
    ),
    ToolMetadata(
        name="risk_assessment",
        description="Assess hiking risk with conservative rule-based guardrails.",
        parameters={
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "weather": {"type": "string"},
                "route": {"type": "string"},
                "experience": {"type": "string"},
                "days": {"type": "integer"},
            },
        },
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=30,
        domain="hiking",
        scenarios=("gear_check", "route_plan", "risk_assessment", "report_export"),
        result_policy="compact",
        hidden=True,
    ),
    ToolMetadata(
        name="trip_report_export",
        description="Export a hiking trip report to Markdown and optionally PDF.",
        parameters={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
                "format": {"type": "string", "enum": ["markdown", "md", "pdf", "both"]},
                "file_name": {"type": "string"},
            },
            "required": ["title", "content"],
        },
        risk_level=RiskLevel.HIGH,
        rate_limit_per_minute=10,
        domain="artifact",
        scenarios=("report_export",),
        auto_allowed=False,
        result_policy="artifact",
        hidden=True,
    ),
])


def _compact_text(value: Any, limit: int = MAX_EVENT_CHARS) -> str:
    if value is None:
        text = ""
    elif isinstance(value, str):
        text = value
    else:
        try:
            text = json.dumps(value, ensure_ascii=False)
        except TypeError:
            text = str(value)
    text = " ".join(text.split())
    if len(text) > limit:
        return text[:limit].rstrip() + "..."
    return text


def _jsonable(value: Any) -> Any:
    try:
        json.dumps(value, ensure_ascii=False)
        return value
    except TypeError:
        return str(value)


def _strip_leading_numbered_lines(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return text.strip()
    stripped = []
    for line in lines:
        stripped.append(re.sub(r"^\d+[.)、]\s*", "", line).strip())
    return "\n".join(line for line in stripped if line).strip()


class AIAgent:
    """LangGraph ReAct Agent with hiking-aware request intake and tool selection."""

    def __init__(self, memory_manager=None, llm_config: RuntimeLlmConfig | None = None):
        self.max_steps = MAX_STEPS
        self.exit_controller = AgentTaskExitController(max_steps=self.max_steps)
        base_url = llm_config.base_url if llm_config and llm_config.base_url else settings.openai_base_url
        api_key = llm_config.api_key if llm_config and llm_config.api_key else settings.openai_api_key
        model = llm_config.model if llm_config and llm_config.model else settings.openai_model
        self.llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=0.7,
        )
        if memory_manager is None and settings.memory_enabled:
            from memory import MemoryConfig

            memory_model = model if llm_config and llm_config.model else None
            config = MemoryConfig(
                compressor_model=memory_model or settings.memory_compressor_model,
                extractor_model=memory_model or settings.memory_extractor_model,
                llm_base_url=base_url,
                llm_api_key=api_key,
                vector_store_path=settings.memory_store_path,
                top_k=settings.memory_top_k,
            )
            self.memory_manager = MemoryManager(config=config)
        else:
            self.memory_manager = memory_manager
        self._memory_context: dict[str, str] = {
            "session_context": "",
            "knowledge_context": "",
        }
        self._query_rewriter = QueryRewriter(
            base_url=base_url,
            api_key=api_key,
            model=model,
        )
        self._query_rewriter.llm = self.llm

    @staticmethod
    def get_tool_registry() -> ToolRegistry:
        return tool_registry

    def _build_system_prompt(self, context: AgentRequestContext, selected_tools: list) -> str:
        slot_lines = []
        for key, value in context.slots.to_dict().items():
            if value is not None:
                slot_lines.append(f"- {key}: {value}")
        slots_text = "\n".join(slot_lines) if slot_lines else "- 未抽取到稳定槽位"
        tool_names = "、".join(tool.name for tool in selected_tools) or "无"
        location_text = "<Location>\n- 未提供当前位置\n</Location>"
        if context.current_location:
            location_items = [
                f"- {key}: {value}"
                for key, value in context.current_location.to_dict().items()
                if value is not None and value != ""
            ]
            location_text = "<Location>\n" + ("\n".join(location_items) or "- 已授权但坐标为空") + "\n</Location>"
        rewritten_text = context.rewritten_query or context.raw_query
        prefetch_text = "<PrefetchedEvidence>\n- 无\n</PrefetchedEvidence>"
        if context.prefetched_tool_results:
            result_lines = [
                json.dumps(result, ensure_ascii=False, default=str)
                for result in context.prefetched_tool_results
            ]
            prefetch_text = "<PrefetchedEvidence>\n" + "\n".join(result_lines) + "\n</PrefetchedEvidence>"

        system_msg = (
            f"{SYSTEM_PROMPT}\n\n"
            "<RuntimeContext>\n"
            f"- raw_query: {context.raw_query}\n"
            f"- rewritten_query: {rewritten_text}\n"
            f"- intent: {context.intent.value}\n"
            f"- scenario: {context.scenario or '未显式指定'}\n"
            f"- selected_tools: {tool_names}\n"
            f"- missing_slots: {', '.join(context.missing_slots) if context.missing_slots else '无'}\n"
            f"- clarifying_question: {context.clarifying_question or '无'}\n"
            "</RuntimeContext>\n\n"
            "<Slots>\n"
            f"{slots_text}\n"
            "</Slots>\n\n"
            f"{location_text}\n\n"
            f"{prefetch_text}\n\n"
            "<ExecutionRules>\n"
            "- 缺少目的地、日期等关键条件时先追问，不要编造路线或天气。\n"
            "- 当用户询问今天/当前位置/附近天气是否适合徒步，且当前定位存在时，不要追问城市；如未预取，先用 geo_lookup 反查定位，再用 weather_lookup 获取天气。\n"
            "- 如当前定位只有 latitude/longitude，调用 geo_lookup 时直接传 latitude 和 longitude；weather_lookup 可使用 geo_lookup 返回的 adcode、city 或坐标。\n"
            "- 如 PrefetchedEvidence 已包含 geo_lookup 和 weather_lookup，本轮不要再次调用它们；可直接回答或最多调用一次 risk_assessment。\n"
            "- 户外安全建议优先引用已预取证据、hiking_knowledge_search、route_research、weather_lookup 等证据。\n"
            "- 最终回答必须是自然中文纯文本，不要 Markdown 标题、粗体符号或编号格式。\n"
            "- 普通徒步场景不要要求终端、下载或任意文件操作。\n"
            "- 生成文档时先组织 Markdown，再按需生成 PDF，并说明路径和影响范围。\n"
            "</ExecutionRules>\n\n"
            f"<NextStep>\n{NEXT_STEP_PROMPT}\n</NextStep>"
        )

        if session_ctx := self._memory_context.get("session_context", ""):
            system_msg += f"\n\n<SessionSummary>\n{session_ctx}\n</SessionSummary>"
        if knowledge_ctx := self._memory_context.get("knowledge_context", ""):
            system_msg += f"\n\n<LongTermMemory>\n{knowledge_ctx}\n</LongTermMemory>"
        return system_msg

    def _make_state_modifier(self, context: AgentRequestContext, selected_tools: list):
        def _state_modifier(state: dict) -> list:
            return [SystemMessage(content=self._build_system_prompt(context, selected_tools))]

        return _state_modifier

    def _rewrite_user_query(self, message: str) -> str:
        try:
            rewritten = self._query_rewriter.humanize_for_answer(message)
        except Exception:
            logger.warning("Agent query rewrite failed", exc_info=True)
            return message
        return rewritten.strip() or message

    def _clean_final_answer(self, text: str) -> str:
        cleaned = clean_display_text(text, preserve_lines=True, keep_list_markers=False)
        cleaned = _strip_leading_numbered_lines(cleaned)
        return cleaned or text.strip()

    def _infer_followup_scenario(self, message: str, history: list | None, scenario: str | None) -> str | None:
        if scenario:
            return scenario
        if self._is_route_recommendation_followup(message, history):
            return AgentIntent.ROUTE_PLAN.value
        return None

    def _is_route_recommendation_followup(self, message: str, history: list | None) -> bool:
        text = " ".join((message or "").strip().split())
        if not text or not any(word == text or word in text for word in AFFIRMATIVE_ROUTE_FOLLOWUP):
            return False
        for msg in reversed(history or []):
            if msg.get("role") != "assistant":
                continue
            content = str(msg.get("content", ""))
            return any(marker in content for marker in ROUTE_FOLLOWUP_MARKERS)
        return False

    def _prefetched_result(self, context: AgentRequestContext, tool_name: str) -> dict[str, Any] | None:
        for item in reversed(context.prefetched_tool_results):
            if not isinstance(item, dict) or item.get("tool") != tool_name:
                continue
            result = item.get("result")
            return result if isinstance(result, dict) else None
        return None

    def _weather_suitability_status(self, weather: dict[str, Any] | None) -> dict[str, Any]:
        if not weather or not weather.get("ok"):
            return {"status": "unknown", "suitable": False, "reason": "没有拿到可用天气数据"}

        text = json.dumps(weather, ensure_ascii=False, default=str)
        if "未接入实时天气 API" in text or "AMAP_API_KEY 未配置" in text:
            return {"status": "unknown", "suitable": False, "reason": "实时天气 API 未配置"}

        bad_markers = ("暴雨", "雷暴", "雷阵雨", "大雨", "中雨", "台风", "冰雹", "大雪", "暴雪", "大风预警", "橙色预警", "红色预警")
        caution_markers = ("小雨", "阵雨", "雾", "霾", "沙尘", "阴")
        if any(marker in text for marker in bad_markers):
            return {"status": "unsafe", "suitable": False, "reason": "天气含强降雨、雷暴、大风或预警信号"}

        wind_power = str(weather.get("wind_power") or weather.get("wind") or "")
        wind_numbers = [int(x) for x in re.findall(r"\d+", wind_power)]
        if wind_numbers and max(wind_numbers) >= 6:
            return {"status": "unsafe", "suitable": False, "reason": "风力偏大，不适合进入山地路线"}

        if any(marker in text for marker in caution_markers):
            return {"status": "caution", "suitable": True, "reason": "天气可出行但需要缩短路线并准备防雨防滑"}

        return {"status": "suitable", "suitable": True, "reason": "天气未见明显硬风险"}

    def _llm_plain_text(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ])
            content = response.content if hasattr(response, "content") else str(response)
            return str(content or "").strip()
        except Exception:
            logger.warning("Direct Agent LLM answer failed", exc_info=True)
            return ""

    def _weather_suitability_text(self, context: AgentRequestContext) -> tuple[str, dict[str, Any]] | None:
        if not self._is_current_location_weather_request(context):
            return None
        geo_result = self._prefetched_result(context, "geo_lookup")
        weather_result = self._prefetched_result(context, "weather_lookup")
        if not weather_result:
            return None

        status = self._weather_suitability_status(weather_result)
        evidence = {
            "location": geo_result,
            "weather": weather_result,
            "status": status,
        }
        answer = self._llm_plain_text(
            "你是户外徒步安全助手。基于证据判断今天是否适合轻量徒步。"
            "只输出自然中文纯文本，先给明确结论，再给2-3个理由。"
            f"如果结论适合，最后必须询问：{ROUTE_RECOMMENDATION_PROMPT}"
            "如果不适合或证据不足，不要推荐路线。",
            "证据：\n" + json.dumps(evidence, ensure_ascii=False, default=str),
        )
        if not answer:
            destination = weather_result.get("city") or weather_result.get("destination") or context.slots.destination or "当前位置"
            if status["status"] == "unknown":
                answer = f"结论：现在还不能可靠判断{destination}今天是否适合徒步。原因是{status['reason']}，请先配置或补充实时天气来源后再决策。"
            elif status["suitable"]:
                weather = weather_result.get("weather") or "天气未注明"
                temperature = weather_result.get("temperature") or "温度未知"
                wind = weather_result.get("wind_power") or weather_result.get("wind") or "风力未知"
                answer = f"结论：今天适合轻量徒步。{destination}当前天气为{weather}，温度{temperature}，风力{wind}，未见明显硬风险。建议选择成熟短线，带足饮水、防晒和雨具。{ROUTE_RECOMMENDATION_PROMPT}"
            else:
                answer = f"结论：今天不建议去徒步。原因是{status['reason']}，建议改期或换成低风险城市步道。"

        answer = self._clean_final_answer(answer)
        if status["suitable"] and ROUTE_RECOMMENDATION_PROMPT not in answer:
            answer = f"{answer.rstrip()} {ROUTE_RECOMMENDATION_PROMPT}"
        return answer, status

    def _route_destination_from_geo(self, context: AgentRequestContext, geo_result: dict[str, Any] | None) -> str:
        primary = (geo_result or {}).get("primary") or {}
        return (
            str(primary.get("district") or "").strip()
            or str(primary.get("city") or "").strip()
            or str(primary.get("name") or "").strip()
            or context.slots.destination
            or (context.current_location.label if context.current_location else "")
            or "当前位置"
        )

    def _is_current_location_route_request(self, context: AgentRequestContext, history: list | None = None) -> bool:
        if context.intent != AgentIntent.ROUTE_PLAN or not context.current_location:
            return False
        text = context.raw_query
        return (
            self._is_route_recommendation_followup(text, history)
            or any(word in text for word in ("推荐路线", "路线推荐", "附近", "周边", "徒步路线"))
        )

    def _route_recommendation_text(self, context: AgentRequestContext) -> tuple[str, dict[str, Any]] | None:
        route_result = self._prefetched_result(context, "route_research")
        if not route_result:
            return None

        evidence = {
            "destination": context.slots.destination,
            "route_research": route_result,
        }
        answer = self._llm_plain_text(
            "你是户外徒步路线推荐助手。基于搜索证据推荐附近路线。"
            "输出自然中文纯文本；每条路线必须包含名称、推荐星级、推荐理由和出发前核验提醒。"
            "如果搜索证据不足，必须明确说明资料不足，不能编造。",
            "证据：\n" + json.dumps(evidence, ensure_ascii=False, default=str),
        )
        routes = route_result.get("recommended_routes") if isinstance(route_result, dict) else None
        if not answer:
            destination = route_result.get("destination") or context.slots.destination or "当前位置"
            if routes:
                lines = [f"我按{destination}附近先搜了路线，可优先看："]
                for route in routes[:5]:
                    lines.append(
                        f"{route.get('name', '候选路线')}，推荐星级 {route.get('rating', '待核验')}，{route.get('reason', '出发前仍需核验路线信息。')}"
                    )
                lines.append("出发前再核验开放状态、天气预警、交通接驳、里程和爬升。")
                answer = "\n".join(lines)
            else:
                answer = f"我已经搜索{destination}附近徒步路线，但没有拿到足够明确的路线名和星级依据。可以换成更具体的区域或景区名，我再继续查。"

        answer = self._clean_final_answer(answer)
        return answer, {"phase": "route_recommendation", "routes_found": len(routes or [])}

    def _is_current_location_weather_request(self, context: AgentRequestContext) -> bool:
        if not context.current_location:
            return False
        if context.intent not in {AgentIntent.RISK_ASSESSMENT, AgentIntent.ROUTE_PLAN}:
            return False
        text = context.raw_query
        weather_words = ("天气", "适合", "能去", "可以去", "徒步吗", "去徒步")
        return any(word in text for word in weather_words)

    def _location_tool_args(self, context: AgentRequestContext) -> dict[str, Any]:
        location = context.current_location
        args: dict[str, Any] = {}
        if location and location.latitude is not None and location.longitude is not None:
            args["latitude"] = location.latitude
            args["longitude"] = location.longitude
        elif context.slots.destination:
            args["destination"] = context.slots.destination
        return args

    def _weather_tool_args(self, context: AgentRequestContext, geo_result: dict[str, Any] | None = None) -> dict[str, Any]:
        location = context.current_location
        primary = (geo_result or {}).get("primary") or {}
        args: dict[str, Any] = {}
        adcode = primary.get("adcode") or (location.adcode if location else None)
        if adcode:
            args["adcode"] = str(adcode)
        if context.slots.destination:
            args["destination"] = context.slots.destination
        if context.slots.date:
            args["date"] = context.slots.date
        if location and location.latitude is not None and location.longitude is not None:
            args["latitude"] = location.latitude
            args["longitude"] = location.longitude
        return args

    async def _prefetch_current_location_weather(self, context: AgentRequestContext) -> list[dict[str, Any]]:
        if not self._is_current_location_weather_request(context):
            return []

        events: list[dict[str, Any]] = []
        geo_args = self._location_tool_args(context)
        if not geo_args:
            return []

        events.append({
            "type": "tool_call",
            "content": f"第 1 步：调用 geo_lookup，参数：{_compact_text(geo_args)}",
            "metadata": {
                "step": 1,
                "tool": "geo_lookup",
                "args": _compact_text(geo_args, MAX_ARGS_CHARS),
                "args_raw": geo_args,
                "prefetch": True,
            },
        })
        try:
            geo_result = await geo_lookup.ainvoke(geo_args)
        except Exception as e:
            geo_result = {"ok": False, "message": f"geo_lookup 调用失败: {str(e)}"}
        safe_geo = _jsonable(geo_result)
        context.prefetched_tool_results.append({"tool": "geo_lookup", "args": geo_args, "result": safe_geo})
        events.append({
            "type": "tool_result",
            "content": f"第 1 步：geo_lookup 返回：{_compact_text(safe_geo)}",
            "metadata": {"step": 1, "tool": "geo_lookup", "prefetch": True},
        })

        weather_args = self._weather_tool_args(context, geo_result if isinstance(geo_result, dict) else None)
        events.append({
            "type": "tool_call",
            "content": f"第 2 步：调用 weather_lookup，参数：{_compact_text(weather_args)}",
            "metadata": {
                "step": 2,
                "tool": "weather_lookup",
                "args": _compact_text(weather_args, MAX_ARGS_CHARS),
                "args_raw": weather_args,
                "prefetch": True,
            },
        })
        try:
            weather_result = await weather_lookup.ainvoke(weather_args)
        except Exception as e:
            weather_result = {"ok": False, "message": f"weather_lookup 调用失败: {str(e)}"}
        safe_weather = _jsonable(weather_result)
        context.prefetched_tool_results.append({"tool": "weather_lookup", "args": weather_args, "result": safe_weather})
        events.append({
            "type": "tool_result",
            "content": f"第 2 步：weather_lookup 返回：{_compact_text(safe_weather)}",
            "metadata": {"step": 2, "tool": "weather_lookup", "prefetch": True},
        })
        return events

    async def _prefetch_current_location_routes(
        self,
        context: AgentRequestContext,
        history: list | None = None,
    ) -> list[dict[str, Any]]:
        if not self._is_current_location_route_request(context, history):
            return []

        events: list[dict[str, Any]] = []
        geo_args = self._location_tool_args(context)
        geo_result: dict[str, Any] | None = None
        if geo_args:
            events.append({
                "type": "tool_call",
                "content": f"第 1 步：调用 geo_lookup，参数：{_compact_text(geo_args)}",
                "metadata": {
                    "step": 1,
                    "tool": "geo_lookup",
                    "args": _compact_text(geo_args, MAX_ARGS_CHARS),
                    "args_raw": geo_args,
                    "prefetch": True,
                },
            })
            try:
                raw_geo_result = await geo_lookup.ainvoke(geo_args)
            except Exception as e:
                raw_geo_result = {"ok": False, "message": f"geo_lookup 调用失败: {str(e)}"}
            safe_geo = _jsonable(raw_geo_result)
            geo_result = safe_geo if isinstance(safe_geo, dict) else None
            context.prefetched_tool_results.append({"tool": "geo_lookup", "args": geo_args, "result": safe_geo})
            events.append({
                "type": "tool_result",
                "content": f"第 1 步：geo_lookup 返回：{_compact_text(safe_geo)}",
                "metadata": {"step": 1, "tool": "geo_lookup", "prefetch": True},
            })

        destination = self._route_destination_from_geo(context, geo_result)
        context.slots.destination = destination
        route_args = {
            "destination": destination,
            "date": context.slots.date or "今天",
            "days": context.slots.days,
            "focus": "徒步路线 推荐 星级",
        }
        route_args = {key: value for key, value in route_args.items() if value is not None}
        events.append({
            "type": "tool_call",
            "content": f"第 {len(events) // 2 + 1} 步：调用 route_research，参数：{_compact_text(route_args)}",
            "metadata": {
                "step": len(events) // 2 + 1,
                "tool": "route_research",
                "args": _compact_text(route_args, MAX_ARGS_CHARS),
                "args_raw": route_args,
                "prefetch": True,
            },
        })
        try:
            route_result = await route_research.ainvoke(route_args)
        except Exception as e:
            route_result = {"ok": False, "message": f"route_research 调用失败: {str(e)}"}
        safe_route = _jsonable(route_result)
        context.prefetched_tool_results.append({"tool": "route_research", "args": route_args, "result": safe_route})
        events.append({
            "type": "tool_result",
            "content": f"第 {len(events) // 2 + 1} 步：route_research 返回：{_compact_text(safe_route)}",
            "metadata": {"step": len(events) // 2 + 1, "tool": "route_research", "prefetch": True},
        })
        return events

    def _build_react_agent(self, context: AgentRequestContext):
        selected_tools = select_tools_for_context(context)
        return create_react_agent(
            model=self.llm,
            tools=apply_tool_confirmation_guards(selected_tools),
            state_modifier=self._make_state_modifier(context, selected_tools),
        )

    def _build_messages(self, message: str, history: list | None = None) -> list:
        messages = []
        if history:
            for msg in history[-10:]:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=message))
        return messages

    async def _inject_memory_context(self, history: list | None, message: str) -> None:
        if self.memory_manager and settings.memory_enabled:
            try:
                ctx = await asyncio.to_thread(self.memory_manager.build_runtime_context, history or [], message)
                self._memory_context["session_context"] = ctx.get("session_context", "")
                self._memory_context["knowledge_context"] = ctx.get("knowledge_context", "")
            except Exception:
                logger.warning("Memory context injection failed", exc_info=True)

    async def _commit_memory(
        self,
        history: list | None,
        message: str,
        final_response: str,
        context: AgentRequestContext,
    ) -> None:
        if not (self.memory_manager and settings.memory_enabled and final_response):
            return
        commit_history = [*(history or []), {"role": "user", "content": message}]
        commit_history.append({"role": "assistant", "content": final_response})
        task_state = {"slots": context.slots.to_dict(), "intent": context.intent.value}
        try:
            await asyncio.to_thread(
                self.memory_manager.commit_interaction,
                commit_history,
                message,
                final_response,
                task_state,
            )
        except Exception:
            logger.warning("Memory commit failed", exc_info=True)

    async def _execute_agent(self, messages: list, context: AgentRequestContext, react_agent=None) -> dict:
        agent = react_agent or self._build_react_agent(context)
        try:
            result = await agent.ainvoke(
                {"messages": messages},
                config={"recursion_limit": self.max_steps * 2 + 2},
            )
            output = ""
            intermediate_steps = []

            for msg in result.get("messages", []):
                content = self._message_content(msg)
                if content:
                    output = content
                if getattr(msg, "type", "") == "tool" or hasattr(msg, "tool_call_id"):
                    step, tool_name = self._tool_result_name(msg, {})
                    exit_result = self.exit_controller.from_tool_result(
                        tool_name,
                        content,
                        current_step=step,
                    )
                    if exit_result:
                        return {
                            "output": exit_result.final_text,
                            "intermediate_steps": intermediate_steps,
                            "exit_status": exit_result.status.value,
                            "exit_reason": exit_result.reason,
                        }
                for call in self._extract_tool_calls(msg):
                    intermediate_steps.append({
                        "tool": call["name"],
                        "args": call["args"],
                    })

            return {
                "output": self._clean_final_answer(output or "任务已完成"),
                "intermediate_steps": intermediate_steps,
                "exit_status": "completed",
                "exit_reason": "agent_completed",
            }
        except Exception as e:
            exit_result = self.exit_controller.from_exception(e, context=context)
            if exit_result:
                return {
                    "output": exit_result.final_text,
                    "intermediate_steps": [],
                    "exit_status": exit_result.status.value,
                    "exit_reason": exit_result.reason,
                }
            logger.exception("Agent execution error")
            return {
                "output": f"执行出错: {str(e)}",
                "intermediate_steps": [],
                "exit_status": "error",
                "exit_reason": "agent_error",
            }

    async def aexecute(
        self,
        message: str,
        history: list | None = None,
        scenario: str | None = None,
        current_location: CurrentLocation | dict | None = None,
    ) -> dict:
        effective_scenario = self._infer_followup_scenario(message, history, scenario)
        context = understand_request(message, scenario=effective_scenario, current_location=current_location)
        context.rewritten_query = self._rewrite_user_query(message)
        await self._prefetch_current_location_weather(context)
        weather_answer = self._weather_suitability_text(context)
        if weather_answer:
            output, status = weather_answer
            await self._commit_memory(history, message, output, context)
            return {
                "output": output,
                "intermediate_steps": context.prefetched_tool_results,
                "exit_status": "completed",
                "exit_reason": "weather_suitability_completed",
                "metadata": status,
            }
        await self._prefetch_current_location_routes(context, history)
        route_answer = self._route_recommendation_text(context)
        if route_answer:
            output, metadata = route_answer
            await self._commit_memory(history, message, output, context)
            return {
                "output": output,
                "intermediate_steps": context.prefetched_tool_results,
                "exit_status": "completed",
                "exit_reason": "route_recommendation_completed",
                "metadata": metadata,
            }
        messages = self._build_messages(context.rewritten_query or message, history)
        await self._inject_memory_context(history, message)
        result = await self._execute_agent(messages, context)
        await self._commit_memory(history, message, result.get("output", ""), context)
        return result

    def _message_content(self, msg: Any) -> str:
        content = getattr(msg, "content", "")
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    parts.append(str(item.get("text", item.get("content", ""))))
                else:
                    parts.append(str(item))
            return "".join(parts).strip()
        return str(content or "").strip()

    def _extract_tool_calls(self, msg: Any) -> list[dict]:
        raw_calls = getattr(msg, "tool_calls", None) or []
        additional = getattr(msg, "additional_kwargs", None) or {}
        raw_calls = raw_calls or additional.get("tool_calls", [])

        calls = []
        for call in raw_calls:
            if not isinstance(call, dict):
                continue
            function = call.get("function") or {}
            name = call.get("name") or function.get("name") or ""
            raw_args = call.get("args")
            if raw_args is None:
                raw_args = call.get("arguments", function.get("arguments", ""))
            call_id = call.get("id") or call.get("tool_call_id") or ""
            args_dict = raw_args if isinstance(raw_args, dict) else None
            calls.append({
                "id": call_id,
                "name": name or "unknown_tool",
                "args": _compact_text(raw_args, MAX_ARGS_CHARS),
                "args_raw": args_dict,
            })
        return calls

    def _iter_update_messages(self, update: Any):
        if isinstance(update, dict):
            for node_name, payload in update.items():
                if isinstance(payload, dict):
                    messages = payload.get("messages", [])
                elif isinstance(payload, list):
                    messages = payload
                else:
                    messages = [payload]
                if not isinstance(messages, list):
                    messages = [messages]
                for msg in messages:
                    yield str(node_name), msg

    def _is_tool_message(self, node_name: str, msg: Any) -> bool:
        msg_type = getattr(msg, "type", "")
        return node_name in {"tools", "tool"} or msg_type == "tool" or hasattr(msg, "tool_call_id")

    def _tool_result_name(self, msg: Any, pending_tools: dict[str, tuple[int, str]]) -> tuple[int, str]:
        call_id = getattr(msg, "tool_call_id", "") or ""
        step, tool_name = pending_tools.get(call_id, (0, ""))
        return step, getattr(msg, "name", "") or tool_name or "tool"

    def _approval_event_from_tool_message(
        self,
        msg: Any,
        pending_tools: dict[str, tuple[int, str]],
        fallback_step: int,
    ) -> dict | None:
        content = self._message_content(msg)
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            return None
        if not isinstance(payload, dict) or payload.get("type") != "approval_required":
            return None

        step, tool_name = self._tool_result_name(msg, pending_tools)
        if step == 0:
            step = fallback_step or 1
        req = tool_registry.get_call_request(tool_name, payload.get("args") or {})
        risk_level = req.risk_level.value if req else RiskLevel.MEDIUM.value
        return {
            "type": "approval_required",
            "content": payload.get("message") or f"工具 {tool_name} 需要用户确认后才能执行。",
            "metadata": {
                "step": step,
                "tool": tool_name,
                "args_raw": payload.get("args") or {},
                "tool_call_id": getattr(msg, "tool_call_id", "") or "",
                "risk_level": risk_level,
                "needs_confirmation": True,
            },
        }

    async def _stream_react_events(self, messages: list, context: AgentRequestContext) -> AsyncGenerator[dict, None]:
        yield {
            "type": "thought",
            "content": "第 1 步：完成请求理解，进入 LangGraph ReAct 循环。",
            "metadata": {
                "phase": "start",
                "max_steps": self.max_steps,
                "intent": context.intent.value,
                "missing_slots": context.missing_slots,
            },
        }

        react_agent = self._build_react_agent(context)
        if not hasattr(react_agent, "astream"):
            result = await self._execute_agent(messages, context, react_agent=react_agent)
            yield {"type": "text", "content": result.get("output", "任务已完成")}
            yield self.exit_controller.done_event(
                result.get("exit_status", "completed"),
                result.get("exit_reason", "agent_completed"),
            )
            return

        pending_tools: dict[str, tuple[int, str]] = {}
        blocked_tool_call_ids: set[str] = set()
        current_step = 0
        final_text = ""
        saw_update = False

        try:
            async for update in react_agent.astream(
                {"messages": messages},
                stream_mode="updates",
                config={"recursion_limit": self.max_steps * 2 + 2},
            ):
                saw_update = True
                for node_name, msg in self._iter_update_messages(update):
                    if self._is_tool_message(node_name, msg):
                        call_id = getattr(msg, "tool_call_id", "") or ""
                        if call_id in blocked_tool_call_ids:
                            continue
                        approval_event = self._approval_event_from_tool_message(
                            msg, pending_tools, current_step
                        )
                        if approval_event:
                            yield approval_event
                            continue
                        content = self._message_content(msg)
                        step, tool_name = self._tool_result_name(msg, pending_tools)
                        if step == 0:
                            step = current_step or 1
                        tool_result_event = {
                            "type": "tool_result",
                            "content": f"第 {step} 步：{tool_name} 返回：{_compact_text(content)}",
                            "metadata": {
                                "step": step,
                                "tool": tool_name,
                                "node": node_name,
                            },
                        }
                        yield tool_result_event
                        exit_result = self.exit_controller.from_tool_result(
                            tool_name,
                            content,
                            current_step=step,
                        )
                        if exit_result:
                            text_event = exit_result.text_event()
                            if text_event:
                                yield text_event
                            yield exit_result.done_event()
                            return
                        continue

                    tool_calls = self._extract_tool_calls(msg)
                    if tool_calls:
                        current_step += 1
                        yield {
                            "type": "thought",
                            "content": f"第 {current_step} 步：模型决定调用工具：{'、'.join(call['name'] for call in tool_calls)}。",
                            "metadata": {
                                "step": current_step,
                                "phase": "tool_selection",
                                "tools": [call["name"] for call in tool_calls],
                            },
                        }
                        for call in tool_calls:
                            if call["id"]:
                                pending_tools[call["id"]] = (current_step, call["name"])
                            call["tool_call_id"] = call["id"]
                            req = tool_registry.get_call_request(call["name"], call.get("args_raw") or {})
                            if req:
                                risk_level = req.risk_level.value
                                needs_confirmation = req.needs_confirmation
                                rate_exceeded = req.rate_limit_remaining is not None and req.rate_limit_remaining == 0
                            else:
                                risk_level = RiskLevel.MEDIUM.value
                                needs_confirmation = False
                                rate_exceeded = False
                            content = f"第 {current_step} 步：调用 {call['name']}，参数：{call['args']}"
                            if rate_exceeded:
                                content += " ⚠️ 该工具已达到速率限制上限，请稍后再试。"
                            yield {
                                "type": "tool_call",
                                "content": content,
                                "metadata": {
                                    "step": current_step,
                                    "tool": call["name"],
                                    "args": call["args"],
                                    "args_raw": call.get("args_raw"),
                                    "tool_call_id": call["id"],
                                    "risk_level": risk_level,
                                    "needs_confirmation": needs_confirmation,
                                    "rate_limit_exceeded": bool(rate_exceeded),
                                },
                            }
                            if needs_confirmation:
                                if call["id"]:
                                    blocked_tool_call_ids.add(call["id"])
                                yield {
                                    "type": "approval_required",
                                    "content": f"工具 {call['name']} 需要用户确认后才能执行。",
                                    "metadata": {
                                        "step": current_step,
                                        "tool": call["name"],
                                        "args_raw": call.get("args_raw") or {},
                                        "tool_call_id": call["id"],
                                        "risk_level": risk_level,
                                        "needs_confirmation": True,
                                    },
                                }
                        continue

                    content = self._message_content(msg)
                    if content:
                        final_text = self._clean_final_answer(content)
                        yield {
                            "type": "text",
                            "content": final_text,
                            "metadata": {"phase": "final_answer", "node": node_name},
                        }

            if not saw_update:
                result = await self._execute_agent(messages, context, react_agent=react_agent)
                final_text = result.get("output", "任务已完成")
                yield {"type": "text", "content": final_text}
                yield self.exit_controller.done_event(
                    result.get("exit_status", "completed"),
                    result.get("exit_reason", "agent_completed"),
                )
                return
            elif not final_text:
                yield {"type": "text", "content": "任务已完成。"}

            yield self.exit_controller.completed().done_event()
        except Exception as e:
            exit_result = self.exit_controller.from_exception(
                e,
                context=context,
                current_step=current_step,
            )
            if exit_result:
                text_event = exit_result.text_event()
                if text_event:
                    yield text_event
                yield exit_result.done_event()
                return
            logger.exception("Agent stream error")
            yield {"type": "error", "content": f"执行出错: {str(e)}"}
            yield self.exit_controller.done_event("error", "agent_error")

    async def aexecute_stream(
        self,
        message: str,
        history: list | None = None,
        scenario: str | None = None,
        current_location: CurrentLocation | dict | None = None,
    ) -> AsyncGenerator[dict, None]:
        effective_scenario = self._infer_followup_scenario(message, history, scenario)
        context = understand_request(message, scenario=effective_scenario, current_location=current_location)
        context.rewritten_query = self._rewrite_user_query(message)
        await self._inject_memory_context(history, message)

        yield {
            "type": "thought",
            "content": "第 0 步：读取会话历史、会话摘要和长期记忆，准备执行 Agent。",
            "metadata": {
                "phase": "memory",
                "intent": context.intent.value,
                "missing_slots": context.missing_slots,
            },
        }
        yield {
            "type": "thought",
            "content": f"第 0 步：已完成 query 改写：{context.rewritten_query}",
            "metadata": {
                "phase": "query_rewrite",
                "raw_query": context.raw_query,
                "rewritten_query": context.rewritten_query,
            },
        }
        for event in await self._prefetch_current_location_weather(context):
            yield event
        weather_answer = self._weather_suitability_text(context)
        if weather_answer:
            output, status = weather_answer
            yield {
                "type": "text",
                "content": output,
                "metadata": {
                    "phase": "weather_suitability",
                    "status": status.get("status"),
                    "should_offer_routes": bool(status.get("suitable")),
                },
            }
            await self._commit_memory(history, message, output, context)
            yield self.exit_controller.done_event(
                "completed",
                "weather_suitability_completed",
                phase="weather_suitability",
            )
            return
        for event in await self._prefetch_current_location_routes(context, history):
            yield event
        route_answer = self._route_recommendation_text(context)
        if route_answer:
            output, metadata = route_answer
            yield {
                "type": "text",
                "content": output,
                "metadata": metadata,
            }
            await self._commit_memory(history, message, output, context)
            yield self.exit_controller.done_event(
                "completed",
                "route_recommendation_completed",
                phase="route_recommendation",
            )
            return
        messages = self._build_messages(context.rewritten_query or message, history)
        assistant_parts: list[str] = []
        async for event in self._stream_react_events(messages, context):
            if event.get("type") == "text":
                assistant_parts.append(event.get("content", ""))
            elif event.get("type") == "done":
                await self._commit_memory(history, message, "".join(assistant_parts).strip(), context)
            yield event
