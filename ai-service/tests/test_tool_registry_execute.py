"""Tests for ToolRegistry.execute_tool — unified tool execution interface."""

import asyncio
import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from tools.risk_classifier import RiskLevel
from tools.tool_registry import ToolMetadata, ToolRegistry


def _make_registry() -> ToolRegistry:
    """Create a fresh ToolRegistry with one low-risk tool."""
    registry = ToolRegistry()
    registry.register(ToolMetadata(
        name="weather_lookup",
        description="Look up weather",
        parameters={"type": "object", "properties": {"destination": {"type": "string"}}},
        risk_level=RiskLevel.LOW,
        rate_limit_per_minute=30,
    ))
    registry.register(ToolMetadata(
        name="file_operation",
        description="File ops",
        parameters={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]},
        risk_level=RiskLevel.HIGH,
        rate_limit_per_minute=20,
        needs_confirmation=True,
    ))
    return registry


@pytest.fixture
def registry():
    return _make_registry()


class TestExecuteToolSuccess:
    @pytest.mark.asyncio
    async def test_success_with_ainvoke(self, registry):
        mock_ainvoke = AsyncMock(return_value={"ok": True, "weather": "晴"})
        mock_tool = SimpleNamespace(ainvoke=mock_ainvoke)
        tool_map = {"weather_lookup": mock_tool}

        result = await registry.execute_tool(
            "weather_lookup", {"destination": "北京"}, tool_map=tool_map,
        )

        assert result["ok"] is True
        assert result["result"]["weather"] == "晴"
        assert result["error"] is None
        assert result["tool_name"] == "weather_lookup"
        assert result["duration_ms"] >= 0
        assert result["validated"] is True
        assert result["needs_confirmation"] is False

    @pytest.mark.asyncio
    async def test_success_with_invoke(self, registry):
        mock_invoke = MagicMock(return_value={"ok": True, "weather": "晴"})
        mock_tool = SimpleNamespace(invoke=mock_invoke)
        tool_map = {"weather_lookup": mock_tool}

        result = await registry.execute_tool(
            "weather_lookup", {"destination": "北京"}, tool_map=tool_map,
        )

        assert result["ok"] is True
        assert result["result"]["weather"] == "晴"


class TestExecuteToolUnknown:
    @pytest.mark.asyncio
    async def test_unknown_tool_returns_error(self, registry):
        result = await registry.execute_tool("nonexistent", {}, tool_map={})
        assert result["ok"] is False
        assert "未知工具" in result["error"]


class TestExecuteToolRateLimit:
    @pytest.mark.asyncio
    async def test_rate_limited_returns_error(self, registry):
        for _ in range(30):
            registry.validate_call("weather_lookup", {"destination": "x"})

        result = await registry.execute_tool(
            "weather_lookup", {"destination": "北京"}, tool_map={},
        )
        assert result["ok"] is False
        assert "速率限制" in result["error"]
        assert result["validated"] is False


class TestExecuteToolSkipValidation:
    @pytest.mark.asyncio
    async def test_skip_validation_bypasses_rate_limit(self, registry):
        for _ in range(30):
            registry.validate_call("weather_lookup", {"destination": "x"})

        mock_ainvoke = AsyncMock(return_value={"ok": True})
        mock_tool = SimpleNamespace(ainvoke=mock_ainvoke)
        tool_map = {"weather_lookup": mock_tool}

        result = await registry.execute_tool(
            "weather_lookup", {"destination": "北京"},
            tool_map=tool_map, skip_validation=True,
        )

        assert result["ok"] is True
        assert result["needs_confirmation"] is False


class TestExecuteToolNoToolMap:
    @pytest.mark.asyncio
    async def test_no_tool_map_returns_error_when_no_instance(self, registry):
        result = await registry.execute_tool(
            "weather_lookup", {"destination": "北京"},
        )
        assert result["ok"] is False
        assert "no registered instance" in result["error"].lower()


class TestExecuteToolException:
    @pytest.mark.asyncio
    async def test_tool_raises_exception(self, registry):
        mock_ainvoke = AsyncMock(side_effect=RuntimeError("API timeout"))
        mock_tool = SimpleNamespace(ainvoke=mock_ainvoke)
        tool_map = {"weather_lookup": mock_tool}

        result = await registry.execute_tool(
            "weather_lookup", {"destination": "北京"}, tool_map=tool_map,
        )

        assert result["ok"] is False
        assert "API timeout" in result["error"]
        assert result["duration_ms"] >= 0


class TestExecuteToolMissingInToolMap:
    @pytest.mark.asyncio
    async def test_tool_not_in_tool_map(self, registry):
        result = await registry.execute_tool(
            "weather_lookup", {"destination": "北京"}, tool_map={},
        )
        assert result["ok"] is False
        assert "not found in tool_map" in result["error"]


class TestExecuteToolNeedsConfirmation:
    @pytest.mark.asyncio
    async def test_high_risk_tool_needs_confirmation(self, registry):
        result = await registry.execute_tool(
            "file_operation", {"path": "/tmp/x"}, tool_map={},
        )
        assert result["needs_confirmation"] is True


class TestExecuteToolResultKeys:
    @pytest.mark.asyncio
    async def test_all_required_keys_present(self, registry):
        mock_ainvoke = AsyncMock(return_value={"ok": True})
        mock_tool = SimpleNamespace(ainvoke=mock_ainvoke)
        tool_map = {"weather_lookup": mock_tool}

        result = await registry.execute_tool(
            "weather_lookup", {}, tool_map=tool_map,
        )

        required_keys = {
            "ok", "result", "error", "tool_name", "args",
            "duration_ms", "step_index", "validated", "needs_confirmation",
        }
        assert required_keys.issubset(result.keys())
