import pytest

from config import settings
from tools.hiking_domain import geo_lookup, route_research, weather_lookup


@pytest.mark.asyncio
async def test_geo_lookup_supports_amap_reverse_geocode(monkeypatch):
    monkeypatch.setattr(settings, "amap_api_key", "amap-key")

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "status": "1",
                "infocode": "10000",
                "regeocode": {
                    "formatted_address": "北京市东城区东华门街道",
                    "addressComponent": {
                        "province": "北京市",
                        "city": [],
                        "district": "东城区",
                        "adcode": "110101",
                    },
                },
            }

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params):
            assert "regeo" in url
            assert params["location"] == "116.4074,39.9042"
            return FakeResponse()

    monkeypatch.setattr("tools.hiking_domain.httpx.AsyncClient", FakeClient)

    result = await geo_lookup.ainvoke({"latitude": 39.9042, "longitude": 116.4074})

    assert result["ok"] is True
    assert result["source"] == "amap_regeo"
    assert result["primary"]["city"] == "北京市"
    assert result["primary"]["adcode"] == "110101"


@pytest.mark.asyncio
async def test_weather_lookup_uses_coordinates_before_amap_weather(monkeypatch):
    monkeypatch.setattr(settings, "amap_api_key", "amap-key")
    calls = []

    class FakeResponse:
        def __init__(self, payload):
            self.payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self.payload

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, params):
            calls.append((url, params))
            if "regeo" in url:
                return FakeResponse({
                    "status": "1",
                    "infocode": "10000",
                    "regeocode": {
                        "formatted_address": "北京市东城区东华门街道",
                        "addressComponent": {
                            "province": "北京市",
                            "city": [],
                            "district": "东城区",
                            "adcode": "110101",
                        },
                    },
                })
            return FakeResponse({
                "status": "1",
                "infocode": "10000",
                "lives": [{
                    "province": "北京市",
                    "city": "东城区",
                    "adcode": "110101",
                    "weather": "晴",
                    "temperature": "23",
                    "winddirection": "北",
                    "windpower": "3",
                    "humidity": "40",
                    "reporttime": "2026-05-19 16:00:00",
                }],
            })

    monkeypatch.setattr("tools.hiking_domain.httpx.AsyncClient", FakeClient)

    result = await weather_lookup.ainvoke({
        "date": "今天",
        "latitude": 39.9042,
        "longitude": 116.4074,
    })

    assert result["ok"] is True
    assert result["weather"] == "晴"
    assert calls[0][1]["location"] == "116.4074,39.9042"
    assert calls[1][1]["city"] == "110101"


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
