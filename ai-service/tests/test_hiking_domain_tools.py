import pytest

from tools.hiking_domain import route_research


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
