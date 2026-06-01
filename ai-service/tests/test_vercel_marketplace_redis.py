import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _reload_config(monkeypatch, **env):
    keys = {
        "VERCEL",
        "REDIS_URL",
        "KV_URL",
        "UPSTASH_REDIS_URL",
        "UPSTASH_REDIS_REST_URL",
        "UPSTASH_REDIS_REST_TOKEN",
        "KV_REST_API_URL",
        "KV_REST_API_TOKEN",
        "DATABASE_URL",
    }
    for key in keys:
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    import config

    importlib.reload(config)
    return config.settings


def test_vercel_defaults_do_not_use_localhost_redis(monkeypatch):
    settings = _reload_config(monkeypatch, VERCEL="1")

    assert settings.redis_url == ""
    assert settings.redis_connection_mode == "none"
    assert settings.redis_configured is False


def test_vercel_marketplace_kv_url_is_accepted(monkeypatch):
    settings = _reload_config(monkeypatch, VERCEL="1", KV_URL="rediss://default:secret@example.upstash.io:6379")

    assert settings.redis_url == "rediss://default:secret@example.upstash.io:6379"
    assert settings.redis_url_source == "KV_URL"
    assert settings.redis_connection_mode == "redis_url"
    assert settings.redis_configured is True


def test_vercel_marketplace_upstash_rest_is_accepted(monkeypatch):
    settings = _reload_config(
        monkeypatch,
        VERCEL="1",
        KV_REST_API_URL="https://example.upstash.io",
        KV_REST_API_TOKEN="secret-token",
    )

    assert settings.redis_rest_url == "https://example.upstash.io"
    assert settings.redis_rest_token == "secret-token"
    assert settings.redis_connection_mode == "upstash_rest"
    assert settings.redis_configured is True


def test_incomplete_upstash_rest_falls_back(monkeypatch):
    settings = _reload_config(monkeypatch, VERCEL="1", KV_REST_API_URL="https://example.upstash.io")

    assert settings.redis_connection_mode == "incomplete_upstash_rest"
    assert settings.redis_configured is False


def test_vercel_neon_database_url_enables_postgres_memory(monkeypatch):
    settings = _reload_config(
        monkeypatch,
        VERCEL="1",
        DATABASE_URL="postgresql://user:secret@example.neon.tech/db",
    )

    assert settings.database_url == "postgresql://user:secret@example.neon.tech/db"
    assert settings.database_url_source == "DATABASE_URL"
    assert settings.postgres_configured is True


def test_redis_chat_memory_uses_upstash_rest_commands():
    from memory.redis_memory import RedisChatMemory

    memory = RedisChatMemory(
        chat_id="rest-chat",
        redis_url="",
        rest_url="https://example.upstash.io",
        rest_token="secret-token",
    )

    responses = [
        MagicMock(json=lambda: {"result": 1}, raise_for_status=lambda: None),
        MagicMock(json=lambda: {"result": "OK"}, raise_for_status=lambda: None),
        MagicMock(
            json=lambda: {
                "result": [
                    '{"role": "user", "content": "hello"}',
                    '{"role": "assistant", "content": "hi"}',
                ]
            },
            raise_for_status=lambda: None,
        ),
    ]
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = None
    mock_client.post.side_effect = responses

    with patch("memory.redis_memory.httpx.Client", return_value=mock_client):
        memory.add_message("user", "hello")
        messages = memory.get_messages()

    assert mock_client.post.call_args_list[0].kwargs["json"] == [
        "RPUSH",
        "chat:rest-chat:messages",
        '{"role": "user", "content": "hello"}',
    ]
    assert mock_client.post.call_args_list[1].kwargs["json"] == [
        "LTRIM",
        "chat:rest-chat:messages",
        -60,
        -1,
    ]
    assert mock_client.post.call_args_list[2].kwargs["json"] == [
        "LRANGE",
        "chat:rest-chat:messages",
        0,
        -1,
    ]
    assert messages == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
    ]


def test_get_chat_memory_selects_redis_when_marketplace_env_present(monkeypatch):
    import memory.factory as factory
    import config
    from config import settings
    from memory.factory import FallbackChatMemory, get_chat_memory

    monkeypatch.setattr(settings, "redis_url", "rediss://default:secret@example.upstash.io:6379")
    monkeypatch.setattr(settings, "redis_rest_url", "")
    monkeypatch.setattr(settings, "redis_rest_token", "")
    monkeypatch.setattr(settings, "database_url_source", "")
    monkeypatch.setattr(config, "settings", settings)
    monkeypatch.setattr(factory, "RedisChatMemory", MagicMock())

    memory = get_chat_memory("marketplace-chat")

    assert isinstance(memory, FallbackChatMemory)


def test_get_chat_memory_falls_back_to_file_when_redis_absent(monkeypatch):
    import config
    from config import settings
    from memory.factory import get_chat_memory
    from memory.file_memory import FileChatMemory

    monkeypatch.setattr(settings, "redis_url", "")
    monkeypatch.setattr(settings, "redis_rest_url", "")
    monkeypatch.setattr(settings, "redis_rest_token", "")
    monkeypatch.setattr(settings, "database_url_source", "")
    monkeypatch.setattr(config, "settings", settings)

    memory = get_chat_memory("file-chat")

    assert isinstance(memory, FileChatMemory)


def test_get_chat_memory_prefers_postgres_when_database_url_present(monkeypatch):
    import memory.factory as factory
    import config
    from config import settings
    from memory.factory import FallbackChatMemory, get_chat_memory

    monkeypatch.setattr(settings, "database_url_source", "DATABASE_URL")
    monkeypatch.setattr(settings, "redis_url", "")
    monkeypatch.setattr(settings, "redis_rest_url", "")
    monkeypatch.setattr(settings, "redis_rest_token", "")
    monkeypatch.setattr(config, "settings", settings)
    monkeypatch.setattr(factory, "PostgresChatMemory", MagicMock())

    memory = get_chat_memory("neon-chat")

    assert isinstance(memory, FallbackChatMemory)
    factory.PostgresChatMemory.assert_called_once_with(chat_id="neon-chat")


def test_vector_store_persists_knowledge_to_redis(monkeypatch, tmp_path):
    import memory.vector_store as vector_store_module
    from config import settings
    from memory.vector_store import VectorStore

    persisted = {}

    class FakeRedisStore:
        def get_json(self, key):
            return persisted.get(key)

        def set_json(self, key, value):
            persisted[key] = value

    class FakeEmbeddings:
        def embed_documents(self, texts):
            return [[0.1, 0.2, 0.3] for _ in texts]

        def embed_query(self, text):
            return [0.1, 0.2, 0.3]

    monkeypatch.setattr(settings, "redis_url", "rediss://default:secret@example.upstash.io:6379")
    monkeypatch.setattr(settings, "redis_rest_url", "")
    monkeypatch.setattr(settings, "redis_rest_token", "")
    monkeypatch.setattr(settings, "embedding_dimensions", 3)
    monkeypatch.setattr(vector_store_module.settings, "embedding_dimensions", 3)
    monkeypatch.setattr(vector_store_module, "FAISS_AVAILABLE", False)
    monkeypatch.setattr(vector_store_module, "RedisCommandStore", lambda: FakeRedisStore())
    monkeypatch.setattr(vector_store_module, "OpenAIEmbeddings", lambda **kwargs: FakeEmbeddings())

    first = VectorStore(store_path=str(tmp_path))
    first.add([{"type": "preference", "subject": "用户", "predicate": "偏好", "object": "轻装"}])

    second = VectorStore(store_path=str(tmp_path))

    assert second.count == 1
    assert second.search("轻装", k=1)[0]["object"] == "轻装"


def test_confirmation_store_persists_pending_records_to_redis():
    from api.confirmation_store import ConfirmationStore

    persisted = {}

    class FakeRedisStore:
        def get_json(self, key):
            return persisted.get(key)

        def set_json(self, key, value):
            persisted[key] = value

    first = ConfirmationStore(persistent_store=FakeRedisStore())
    cid = first.add("file_operation", {"path": "report.md"}, chat_id="chat-redis", step=2)

    second = ConfirmationStore(persistent_store=FakeRedisStore())
    rec = second.get(cid)

    assert rec is not None
    assert rec.tool_name == "file_operation"
    assert rec.args == {"path": "report.md"}
    assert [item.confirmation_id for item in second.get_pending_by_chat("chat-redis")] == [cid]
