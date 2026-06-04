import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from config import settings
from mcp.capabilities import resolve_hiking_capability


@pytest.mark.asyncio
async def test_resolve_hiking_capability_calls_mapped_mcp_tool(monkeypatch):
    monkeypatch.setattr(settings, "mcp_servers", {"amap": {"command": "amap-mcp"}}, raising=False)
    monkeypatch.setattr(
        settings,
        "mcp_capability_map",
        {"weather": {"server": "amap", "tool": "weather"}},
        raising=False,
    )
    calls = []

    class FakeRuntime:
        async def call_tool(self, server, tool, arguments):
            calls.append((server, tool, arguments))
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps({
                        "weather": "晴",
                        "temperature": "23",
                        "adcode": "110101",
                    }, ensure_ascii=False),
                }]
            }

    monkeypatch.setattr("mcp.capabilities.get_mcp_runtime", lambda: FakeRuntime())

    result = await resolve_hiking_capability("weather", {"destination": "北京"})

    assert result["ok"] is True
    assert result["source"] == "mcp:amap:weather"
    assert result["weather"] == "晴"
    assert result["temperature"] == "23"
    assert calls == [("amap", "weather", {"destination": "北京"})]


@pytest.mark.asyncio
async def test_resolve_hiking_capability_preserves_mcp_tool_errors(monkeypatch):
    monkeypatch.setattr(settings, "mcp_servers", {"amap": {"command": "amap-mcp"}}, raising=False)
    monkeypatch.setattr(
        settings,
        "mcp_capability_map",
        {"weather": {"server": "amap", "tool": "weather"}},
        raising=False,
    )

    class FakeRuntime:
        async def call_tool(self, server, tool, arguments):
            return {
                "isError": True,
                "message": "weather unavailable",
                "content": [{"type": "text", "text": "weather unavailable"}],
            }

    monkeypatch.setattr("mcp.capabilities.get_mcp_runtime", lambda: FakeRuntime())

    result = await resolve_hiking_capability("weather", {"destination": "北京"})

    assert result["ok"] is False
    assert result["source"] == "mcp.weather"
    assert "weather unavailable" in result["message"]
