"""Tests for tools.tool_registry — ToolCollection unified interface.

The ToolCollection extends ToolRegistry to also hold tool instances,
so execute_tool no longer needs an external tool_map parameter.
MCP tools can be registered through the same register_tool() interface.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from tools.risk_classifier import RiskLevel
from tools.tool_registry import ToolMetadata, ToolRegistry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _metadata(name: str = "test_tool", **overrides) -> ToolMetadata:
    defaults = dict(
        name=name,
        description=f"Test tool: {name}",
        parameters={"type": "object", "properties": {}},
        risk_level=RiskLevel.LOW,
        auto_allowed=True,
    )
    defaults.update(overrides)
    return ToolMetadata(**defaults)


def _mock_tool(name: str = "test_tool") -> MagicMock:
    """Create a mock tool with ainvoke."""
    tool = MagicMock()
    tool.name = name
    tool.ainvoke = AsyncMock(return_value=f"{name} result")
    return tool


# ---------------------------------------------------------------------------
# Test: ToolRegistry.register_tool (unified registration)
# ---------------------------------------------------------------------------

class TestToolRegistryRegisterTool:
    """register_tool registers both metadata and instance in one call."""

    def test_register_tool_stores_metadata_and_instance(self):
        registry = ToolRegistry()
        tool = _mock_tool("weather_lookup")
        metadata = _metadata("weather_lookup")
        registry.register_tool("weather_lookup", tool, metadata)

        assert registry.get("weather_lookup") is not None
        assert registry.get_tool_instance("weather_lookup") is tool

    def test_register_tool_duplicate_name_raises(self):
        registry = ToolRegistry()
        tool = _mock_tool("weather_lookup")
        metadata = _metadata("weather_lookup")
        registry.register_tool("weather_lookup", tool, metadata)

        with pytest.raises(ValueError, match="已注册"):
            registry.register_tool("weather_lookup", tool, metadata)

    def test_register_tool_without_instance_stores_none(self):
        """Registering metadata only (no instance) should still work."""
        registry = ToolRegistry()
        metadata = _metadata("geo_lookup")
        registry.register_tool("geo_lookup", None, metadata)

        assert registry.get("geo_lookup") is not None
        assert registry.get_tool_instance("geo_lookup") is None


# ---------------------------------------------------------------------------
# Test: ToolRegistry.get_tool_instance
# ---------------------------------------------------------------------------

class TestToolRegistryGetToolInstance:
    def test_get_tool_instance_returns_registered_tool(self):
        registry = ToolRegistry()
        tool = _mock_tool("weather_lookup")
        registry.register_tool("weather_lookup", tool, _metadata("weather_lookup"))

        assert registry.get_tool_instance("weather_lookup") is tool

    def test_get_tool_instance_unknown_returns_none(self):
        registry = ToolRegistry()
        assert registry.get_tool_instance("unknown_tool") is None


# ---------------------------------------------------------------------------
# Test: ToolRegistry.execute_tool without tool_map
# ---------------------------------------------------------------------------

class TestToolRegistryExecuteToolUnified:
    """execute_tool should work without tool_map when instances are registered."""

    @pytest.mark.asyncio
    async def test_execute_tool_with_registered_instance(self):
        registry = ToolRegistry()
        tool = _mock_tool("weather_lookup")
        tool.ainvoke = AsyncMock(return_value="晴，23°C")
        registry.register_tool("weather_lookup", tool, _metadata("weather_lookup"))

        result = await registry.execute_tool("weather_lookup", {"adcode": "110101"})
        assert result["ok"] is True
        assert result["result"] == "晴，23°C"
        assert result["tool_name"] == "weather_lookup"

    @pytest.mark.asyncio
    async def test_execute_tool_without_instance_returns_error(self):
        """When no instance is registered and no tool_map provided, return error."""
        registry = ToolRegistry()
        registry.register_tool("geo_lookup", None, _metadata("geo_lookup"))

        result = await registry.execute_tool("geo_lookup", {"latitude": 39.9})
        assert result["ok"] is False
        assert "not found" in result["error"].lower() or "no registered instance" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_execute_tool_with_tool_map_still_works(self):
        """Backward compat: tool_map parameter should still work."""
        registry = ToolRegistry()
        metadata = _metadata("weather_lookup")
        registry.register(metadata)  # Old-style registration

        tool = _mock_tool("weather_lookup")
        tool.ainvoke = AsyncMock(return_value="晴，23°C")
        tool_map = {"weather_lookup": tool}

        result = await registry.execute_tool("weather_lookup", {"adcode": "110101"}, tool_map=tool_map)
        assert result["ok"] is True
        assert result["result"] == "晴，23°C"

    @pytest.mark.asyncio
    async def test_execute_tool_registered_instance_takes_priority_over_tool_map(self):
        """When both registered instance and tool_map exist, use registered instance."""
        registry = ToolRegistry()
        tool_a = _mock_tool("weather_lookup")
        tool_a.ainvoke = AsyncMock(return_value="from registered instance")
        registry.register_tool("weather_lookup", tool_a, _metadata("weather_lookup"))

        tool_b = _mock_tool("weather_lookup")
        tool_b.ainvoke = AsyncMock(return_value="from tool_map")

        result = await registry.execute_tool("weather_lookup", {"adcode": "110101"})
        assert result["ok"] is True
        assert result["result"] == "from registered instance"

    @pytest.mark.asyncio
    async def test_execute_tool_validates_before_executing(self):
        """Validation (rate limit, etc.) should still run before execution."""
        registry = ToolRegistry()
        tool = _mock_tool("weather_lookup")
        registry.register_tool(
            "weather_lookup", tool,
            _metadata("weather_lookup", rate_limit_per_minute=1),
        )

        # First call should succeed
        result1 = await registry.execute_tool("weather_lookup", {"adcode": "110101"})
        assert result1["ok"] is True

        # Exhaust rate limit
        registry.validate_call("weather_lookup", {})

        # Second call should fail due to rate limit
        result2 = await registry.execute_tool("weather_lookup", {"adcode": "110101"})
        assert result2["ok"] is False
        assert "速率限制" in result2["error"]


# ---------------------------------------------------------------------------
# Test: ToolRegistry.register_many_tools (batch registration)
# ---------------------------------------------------------------------------

class TestToolRegistryRegisterManyTools:
    def test_register_many_tools_registers_all(self):
        registry = ToolRegistry()
        tool_a = _mock_tool("weather_lookup")
        tool_b = _mock_tool("geo_lookup")

        registry.register_many_tools([
            ("weather_lookup", tool_a, _metadata("weather_lookup")),
            ("geo_lookup", tool_b, _metadata("geo_lookup")),
        ])

        assert registry.get("weather_lookup") is not None
        assert registry.get("geo_lookup") is not None
        assert registry.get_tool_instance("weather_lookup") is tool_a
        assert registry.get_tool_instance("geo_lookup") is tool_b


# ---------------------------------------------------------------------------
# Test: MCP tool registration (mock)
# ---------------------------------------------------------------------------

class TestMCPToolRegistration:
    """MCP tools can be registered through the same interface."""

    @pytest.mark.asyncio
    async def test_mcp_tool_registration_and_execution(self):
        """An MCP tool (with ainvoke) can be registered and executed."""
        registry = ToolRegistry()

        # Simulate an MCP tool — just an object with ainvoke
        mcp_tool = MagicMock()
        mcp_tool.ainvoke = AsyncMock(return_value={"flights": ["CA1234"]})

        registry.register_tool(
            "mcp_flight_search",
            mcp_tool,
            ToolMetadata(
                name="mcp_flight_search",
                description="Search flights via MCP",
                parameters={"type": "object", "properties": {"from": {"type": "string"}}},
                risk_level=RiskLevel.LOW,
                domain="mcp",
                auto_allowed=True,
            ),
        )

        result = await registry.execute_tool("mcp_flight_search", {"from": "PEK"})
        assert result["ok"] is True
        assert result["result"] == {"flights": ["CA1234"]}

    @pytest.mark.asyncio
    async def test_mcp_tool_with_invoke_fallback(self):
        """An MCP tool with only invoke (not ainvoke) should also work."""
        registry = ToolRegistry()

        # Create a tool that only has invoke, not ainvoke
        class SyncOnlyTool:
            def invoke(self, args):
                return "sync result"

        mcp_tool = SyncOnlyTool()

        registry.register_tool(
            "mcp_sync_tool",
            mcp_tool,
            _metadata("mcp_sync_tool"),
        )

        result = await registry.execute_tool("mcp_sync_tool", {})
        assert result["ok"] is True
        assert result["result"] == "sync result"
