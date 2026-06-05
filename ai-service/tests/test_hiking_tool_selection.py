from agent.agent import (
    AVAILABLE_TOOL_MAP,
    AVAILABLE_TOOLS,
    OPENMANUS_TOOL_NAMES,
    validate_tool_configuration,
)


def tool_names(tools):
    return {tool.name for tool in tools}


def test_openmanus_tool_surface_exposes_local_agent_tools_without_mcp_aliases():
    names = tool_names(AVAILABLE_TOOLS)

    assert names == set(OPENMANUS_TOOL_NAMES)
    assert "web_search" in names
    assert "weather_lookup" not in names
    assert "geo_lookup" not in names
    assert "route_research" in names
    assert "hiking_knowledge_search" in names
    assert "terminate" in names


def test_all_openmanus_tool_names_are_addressable_by_name():
    assert set(OPENMANUS_TOOL_NAMES).issubset(set(AVAILABLE_TOOL_MAP))


def test_tool_configuration_validation_reports_current_setup_ok():
    result = validate_tool_configuration()

    assert result["ok"] is True
    assert result["available_count"] == 12
    assert result["registered_count"] == 12
    assert result["openmanus_tool_count"] == 12
    assert result["issues"] == []
