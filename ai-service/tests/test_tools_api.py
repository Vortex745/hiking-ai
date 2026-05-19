import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app


def _tool_names(payload):
    return {item["function"]["name"] for item in payload["tools"]}


def test_tools_api_lists_visible_tools_by_default():
    client = TestClient(app)

    response = client.get("/api/v1/tools")

    assert response.status_code == 200
    data = response.json()
    names = _tool_names(data)
    assert data["count"] == 7
    assert "web_search" in names
    assert "terminal" in names
    assert "hiking_knowledge_search" not in names

    terminal = next(item for item in data["tools"] if item["function"]["name"] == "terminal")
    assert terminal["function"]["risk_level"] == "critical"
    assert terminal["function"]["needs_confirmation"] is True
    assert terminal["function"]["hidden"] is False

    terminate = next(item for item in data["tools"] if item["function"]["name"] == "terminate")
    assert terminate["function"]["risk_level"] == "high"
    assert terminate["function"]["needs_confirmation"] is False


def test_tools_api_can_include_hidden_domain_tools():
    client = TestClient(app)

    response = client.get("/api/v1/tools?include_hidden=true")

    assert response.status_code == 200
    data = response.json()
    names = _tool_names(data)
    assert data["count"] == 14
    assert "hiking_knowledge_search" in names
    assert "trip_report_export" in names

    hiking_tool = next(
        item for item in data["tools"] if item["function"]["name"] == "hiking_knowledge_search"
    )
    assert hiking_tool["function"]["domain"] == "hiking"
    assert hiking_tool["function"]["hidden"] is True


def test_tools_health_reports_registry_and_mcp_readiness():
    client = TestClient(app)

    response = client.get("/api/v1/tools/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["tools_total"] == 14
    assert data["visible_tools"] == 7
    assert data["hidden_tools"] == 7
    assert data["configuration"]["ok"] is True
    assert data["mcp"]["configured"] is False
    assert "amap_api_key" in data["external_keys"]
