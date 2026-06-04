import pytest

from config import settings
from tools.hiking_domain import geo_lookup, route_research, weather_lookup


@pytest.mark.asyncio
async def test_weather_lookup_returns_unavailable_when_mcp_capability_missing(monkeypatch):
    monkeypatch.setattr(settings, "mcp_servers", {}, raising=False)
    monkeypatch.setattr(settings, "mcp_capability_map", {}, raising=False)

    result = await weather_lookup.ainvoke({"destination": "北京", "date": "今天"})

    assert result["ok"] is False
    assert result["source"] == "mcp.weather"
    assert "MCP" in result["message"]


@pytest.mark.asyncio
async def test_weather_lookup_uses_mcp_capability_alias(monkeypatch):
    monkeypatch.setattr(settings, "mcp_servers", {"amap": {"command": "amap-mcp"}}, raising=False)
    monkeypatch.setattr(
        settings,
        "mcp_capability_map",
        {"weather": {"server": "amap", "tool": "weather"}},
        raising=False,
    )
    calls = []

    async def fake_resolve(capability, arguments):
        calls.append((capability, arguments))
        return {
            "ok": True,
            "source": "mcp:amap:weather",
            "weather": "晴",
            "temperature": "23",
        }

    monkeypatch.setattr("tools.hiking_domain.resolve_hiking_capability", fake_resolve)

    result = await weather_lookup.ainvoke({"destination": "北京", "date": "今天"})

    assert result["ok"] is True
    assert result["source"] == "mcp:amap:weather"
    assert result["weather"] == "晴"
    assert calls == [("weather", {
        "destination": "北京",
        "date": "今天",
        "adcode": "",
        "latitude": None,
        "longitude": None,
    })]


@pytest.mark.asyncio
async def test_geo_lookup_returns_unavailable_when_mcp_capability_missing(monkeypatch):
    monkeypatch.setattr(settings, "mcp_servers", {}, raising=False)
    monkeypatch.setattr(settings, "mcp_capability_map", {}, raising=False)

    result = await geo_lookup.ainvoke({"latitude": 39.9042, "longitude": 116.4074})

    assert result["ok"] is False
    assert result["source"] == "mcp.reverse_geocode"
    assert "MCP" in result["message"]


@pytest.mark.asyncio
async def test_geo_lookup_uses_mcp_capability_alias(monkeypatch):
    monkeypatch.setattr(settings, "mcp_servers", {"amap": {"command": "amap-mcp"}}, raising=False)
    monkeypatch.setattr(
        settings,
        "mcp_capability_map",
        {"reverse_geocode": {"server": "amap", "tool": "regeo"}},
        raising=False,
    )
    calls = []

    async def fake_resolve(capability, arguments):
        calls.append((capability, arguments))
        return {
            "ok": True,
            "source": "mcp:amap:regeo",
            "primary": {"city": "北京市", "adcode": "110101"},
        }

    monkeypatch.setattr("tools.hiking_domain.resolve_hiking_capability", fake_resolve)

    result = await geo_lookup.ainvoke({"latitude": 39.9042, "longitude": 116.4074})

    assert result["ok"] is True
    assert result["source"] == "mcp:amap:regeo"
    assert result["primary"]["adcode"] == "110101"
    assert calls == [("reverse_geocode", {
        "destination": "",
        "latitude": 39.9042,
        "longitude": 116.4074,
    })]


@pytest.mark.asyncio
async def test_weather_lookup_passes_coordinates_to_mcp_alias(monkeypatch):
    monkeypatch.setattr(settings, "mcp_servers", {"amap": {"command": "amap-mcp"}}, raising=False)
    monkeypatch.setattr(
        settings,
        "mcp_capability_map",
        {"weather": {"server": "amap", "tool": "weather"}},
        raising=False,
    )
    calls = []

    async def fake_resolve(capability, arguments):
        calls.append((capability, arguments))
        return {
            "ok": True,
            "source": "mcp:amap:weather",
            "weather": "晴",
            "temperature": "23",
        }

    monkeypatch.setattr("tools.hiking_domain.resolve_hiking_capability", fake_resolve)

    result = await weather_lookup.ainvoke({
        "date": "今天",
        "latitude": 39.9042,
        "longitude": 116.4074,
    })

    assert result["ok"] is True
    assert result["source"] == "mcp:amap:weather"
    assert calls == [("weather", {
        "destination": "",
        "date": "今天",
        "adcode": "",
        "latitude": 39.9042,
        "longitude": 116.4074,
    })]


@pytest.mark.asyncio
async def test_route_research_uses_search_engine_and_builds_route_ratings(monkeypatch):
    calls = []

    async def fake_web_search(payload):
        calls.append(payload["query"])
        return "白云山风景区徒步路线成熟，六片山短线适合半日徒步，火炉山森林公园步道适合新手。"

    monkeypatch.setattr("tools.hiking_domain.web_search", type("FakeSearch", (), {"ainvoke": staticmethod(fake_web_search)}))

    result = await route_research.ainvoke({
        "destination": "白云区",
        "date": "今天",
        "focus": "推荐 星级",
    })

    assert result["ok"] is True
    assert len(calls) >= 1
    assert any("白云区 徒步 路线 推荐 星级" in query for query in calls)
    assert result["search_results"]
    assert result["recommended_routes"]
    assert result["recommended_routes"][0]["rating"].endswith("/5")
