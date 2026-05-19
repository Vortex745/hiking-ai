"""Tests for model and embedding configuration."""

import os
import sys
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import Settings
from memory import vector_store as memory_vector_store
from rag import retriever as retriever_module


def test_settings_loads_independent_embedding_config(monkeypatch):
    """Embedding settings should not be tied to the chat model config."""

    monkeypatch.setenv("OPENAI_API_KEY", "chat-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://chat.example/v1")
    monkeypatch.setenv("OPENAI_MODEL", "chat-model")
    monkeypatch.setenv("EMBEDDING_API_KEY", "embedding-key")
    monkeypatch.setenv("EMBEDDING_BASE_URL", "https://embed.example/v1")
    monkeypatch.setenv("EMBEDDING_MODEL", "embed-model")
    monkeypatch.setenv("EMBEDDING_DIMENSIONS", "4096")

    settings = Settings().load()

    assert settings.openai_api_key == "chat-key"
    assert settings.embedding_api_key == "embedding-key"
    assert settings.embedding_base_url == "https://embed.example/v1"
    assert settings.embedding_model == "embed-model"
    assert settings.embedding_dimensions == 4096


def test_settings_loads_without_global_chat_api_key(monkeypatch):
    """AI service should still start when only retrieval model config exists."""

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("EMBEDDING_API_KEY", "embedding-key")
    monkeypatch.setenv("EMBEDDING_BASE_URL", "https://embed.example/v1")
    monkeypatch.setenv("EMBEDDING_MODEL", "embed-model")

    settings = Settings().load()

    assert settings.openai_api_key == ""
    assert settings.embedding_api_key == "embedding-key"
    assert settings.embedding_base_url == "https://embed.example/v1"
    assert settings.embedding_model == "embed-model"


def test_settings_loads_independent_rerank_config(monkeypatch):
    """Rerank settings should be configurable independently from chat and embedding."""

    monkeypatch.setenv("OPENAI_API_KEY", "chat-key")
    monkeypatch.setenv("EMBEDDING_API_KEY", "embedding-key")
    monkeypatch.setenv("EMBEDDING_BASE_URL", "https://embed.example/v1")
    monkeypatch.setenv("RERANK_API_KEY", "rerank-key")
    monkeypatch.setenv("RERANK_BASE_URL", "https://rerank.example/v1")
    monkeypatch.setenv("RERANK_MODEL", "rerank-model")
    monkeypatch.setenv("RERANK_TOP_K", "6")
    monkeypatch.setenv("RERANK_TIMEOUT_SECONDS", "8")

    settings = Settings().load()

    assert settings.rerank_api_key == "rerank-key"
    assert settings.rerank_base_url == "https://rerank.example/v1"
    assert settings.rerank_model == "rerank-model"
    assert settings.rerank_top_k == 6
    assert settings.rerank_timeout_seconds == 8


def test_rag_retriever_uses_embedding_config(monkeypatch):
    """RAG retriever should build embeddings from embedding-specific settings."""

    captured = {}

    class Embeddings:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(retriever_module.settings, "embedding_base_url", "https://embed.example/v1")
    monkeypatch.setattr(retriever_module.settings, "embedding_api_key", "embedding-key")
    monkeypatch.setattr(retriever_module.settings, "embedding_model", "embed-model")
    monkeypatch.setattr(retriever_module, "OpenAIEmbeddings", Embeddings)

    retriever_module.VectorStoreRetriever()

    assert captured["base_url"] == "https://embed.example/v1"
    assert captured["api_key"] == "embedding-key"
    assert captured["model"] == "embed-model"


def test_memory_vector_store_uses_embedding_config(monkeypatch, tmp_path):
    """Memory vector store should share the same embedding config."""

    captured = {}

    class Embeddings:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(memory_vector_store.settings, "embedding_base_url", "https://embed.example/v1")
    monkeypatch.setattr(memory_vector_store.settings, "embedding_api_key", "embedding-key")
    monkeypatch.setattr(memory_vector_store.settings, "embedding_model", "embed-model")
    monkeypatch.setattr(memory_vector_store, "OpenAIEmbeddings", Embeddings)

    memory_vector_store.VectorStore(store_path=str(tmp_path))

    assert captured["base_url"] == "https://embed.example/v1"
    assert captured["api_key"] == "embedding-key"
    assert captured["model"] == "embed-model"
