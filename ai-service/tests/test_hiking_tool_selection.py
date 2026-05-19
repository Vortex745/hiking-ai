from agent.agent import AVAILABLE_TOOL_MAP, select_tools_for_context, validate_tool_configuration
from agent.intake import AgentIntent, understand_request


def tool_names(tools):
    return {tool.name for tool in tools}


def test_gear_check_exposes_only_hiking_safe_tools():
    context = understand_request("新手单日徒步装备清单")

    names = tool_names(select_tools_for_context(context))

    assert "hiking_knowledge_search" in names
    assert "gear_checklist" in names
    assert "risk_assessment" in names
    assert "terminate" in names
    assert "terminal" not in names
    assert "file_operation" not in names
    assert "resource_download" not in names


def test_current_location_weather_question_exposes_geo_and_weather_tools():
    context = understand_request(
        "今天的天气适合去徒步吗",
        current_location={"latitude": 39.9042, "longitude": 116.4074},
    )

    names = tool_names(select_tools_for_context(context))

    assert context.intent == AgentIntent.RISK_ASSESSMENT
    assert "geo_lookup" in names
    assert "weather_lookup" in names
    assert "risk_assessment" in names
    assert "terminal" not in names


def test_prefetched_current_location_weather_reduces_followup_tools():
    context = understand_request(
        "今天的天气适合去徒步吗",
        current_location={"latitude": 39.9042, "longitude": 116.4074},
    )
    context.prefetched_tool_results.extend([
        {"tool": "geo_lookup", "result": {"ok": True}},
        {"tool": "weather_lookup", "result": {"ok": True, "weather": "晴"}},
    ])

    names = tool_names(select_tools_for_context(context))

    assert names == {"risk_assessment", "terminate"}


def test_general_chat_exposes_only_termination_control():
    context = understand_request("你好")

    names = tool_names(select_tools_for_context(context))

    assert names == {"terminate"}


def test_report_export_exposes_export_tools_but_not_terminal():
    context = understand_request("把武功山路线整理成 PDF")

    names = tool_names(select_tools_for_context(context))

    assert context.intent == AgentIntent.REPORT_EXPORT
    assert "trip_report_export" in names
    assert "generate_pdf" in names
    assert "file_operation" in names
    assert "terminal" not in names


def test_all_registered_tool_functions_are_addressable_by_name():
    required = {
        "hiking_knowledge_search",
        "gear_checklist",
        "risk_assessment",
        "route_research",
        "terminate",
    }

    assert required.issubset(set(AVAILABLE_TOOL_MAP))


def test_tool_configuration_validation_reports_current_setup_ok():
    result = validate_tool_configuration()

    assert result["ok"] is True
    assert result["available_count"] == 14
    assert result["registered_count"] == 14
    assert result["issues"] == []
