import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from main import app
from config import settings


def test_chat_health_unconfigured(monkeypatch):
    """If openai_api_key is empty, chat health check should return unconfigured directly."""
    monkeypatch.setattr(settings, "openai_api_key", "")

    client = TestClient(app)
    response = client.get("/api/v1/chat/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "unconfigured"
    assert data["module"] == "agent"
    assert data["service"] == "ai-service"


def test_chat_health_agent_raises_key_error(monkeypatch):
    """If agent initialization raises an error indicating missing api key, report as unconfigured gracefully."""
    monkeypatch.setattr(settings, "openai_api_key", "dummy-key")

    from api import chat as chat_api

    class BrokenAIAgent:
        def __init__(self, *args, **kwargs):
            raise ValueError("The api_key client option must be set")

    monkeypatch.setattr(chat_api, "AIAgent", BrokenAIAgent)

    client = TestClient(app)
    response = client.get("/api/v1/chat/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "unconfigured"
    assert "api_key" in data["detail"]


def test_chat_sse_missing_openai_key_returns_stream_error(monkeypatch):
    """Missing Agent LLM key should not produce HTTP 500 before the SSE stream starts."""
    monkeypatch.setattr(settings, "openai_api_key", "")
    monkeypatch.setattr(settings, "memory_enabled", False)

    client = TestClient(app)
    response = client.post(
        "/api/v1/chat/sse",
        json={"chat_id": "missing-key-sse", "message": "今天的天气适合去徒步吗"},
    )

    assert response.status_code == 200
    body = response.text
    assert '"type": "error"' in body
    assert "OPENAI_API_KEY" in body
    assert '"type": "done"' in body


def test_chat_sse_accepts_runtime_llm_settings_without_env_key(monkeypatch):
    """Agent chat should use LLM settings saved by the frontend when env key is empty."""
    monkeypatch.setattr(settings, "openai_api_key", "")
    monkeypatch.setattr(settings, "memory_enabled", False)

    captured = {}

    class FakeAgent:
        def __init__(self, *args, llm_config=None, **kwargs):
            captured["llm_config"] = llm_config

        async def aexecute_stream(self, message, history=None, scenario=None):
            yield {"type": "text", "content": f"ok:{scenario}"}
            yield {"type": "done", "content": ""}

    from api import chat as chat_api

    monkeypatch.setattr(chat_api, "AIAgent", FakeAgent)

    client = TestClient(app)
    response = client.post(
        "/api/v1/chat/sse",
        json={
            "chat_id": "runtime-llm-sse",
            "message": "今天的天气适合去徒步吗",
            "scenario": "route_plan",
            "model_settings": {
                "llm": {
                    "base_url": "https://runtime.example/v1",
                    "api_key": "runtime-key",
                    "model": "runtime-model",
                }
            },
        },
    )

    assert response.status_code == 200
    assert "ok:route_plan" in response.text
    assert captured["llm_config"].api_key == "runtime-key"
    assert captured["llm_config"].base_url == "https://runtime.example/v1"
    assert captured["llm_config"].model == "runtime-model"


def test_chat_sync_missing_openai_key_returns_503(monkeypatch):
    """Sync chat should expose missing model config as a service config error."""
    monkeypatch.setattr(settings, "openai_api_key", "")
    monkeypatch.setattr(settings, "memory_enabled", False)

    client = TestClient(app)
    response = client.post(
        "/api/v1/chat/sync",
        json={"chat_id": "missing-key-sync", "message": "今天的天气适合去徒步吗"},
    )

    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]
