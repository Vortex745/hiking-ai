import os
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Ensure OPENAI_API_KEY is set for config import
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "test-key-for-testing"

from fastapi.testclient import TestClient
from main import app
from config import settings
from agent.agent import AIAgent
from api.models import RuntimeLlmConfig
from memory import MemoryManager, MemoryConfig


def test_agent_memory_initialization_enabled(monkeypatch):
    """When memory is enabled in settings, AIAgent should initialize a standard MemoryManager with config."""
    monkeypatch.setattr(settings, "memory_enabled", True)
    monkeypatch.setattr(settings, "memory_store_path", "./test_memory_store")
    monkeypatch.setattr(settings, "memory_top_k", 3)
    monkeypatch.setattr(settings, "memory_compressor_model", "test-compressor")
    monkeypatch.setattr(settings, "memory_extractor_model", "test-extractor")

    # Mock the LLM initialization to avoid calling actual ChatOpenAI
    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent"):
        agent = AIAgent()
        assert agent.memory_manager is not None
        assert isinstance(agent.memory_manager, MemoryManager)
        assert agent.memory_manager.config.vector_store_path == "./test_memory_store"
        assert agent.memory_manager.config.top_k == 3
        assert agent.memory_manager.config.compressor_model == "test-compressor"
        assert agent.memory_manager.config.extractor_model == "test-extractor"


def test_agent_memory_uses_runtime_llm_config_when_env_key_missing(monkeypatch):
    """Runtime LLM settings should also configure memory compression/extraction."""
    monkeypatch.setattr(settings, "openai_api_key", "")
    monkeypatch.setattr(settings, "memory_enabled", True)
    monkeypatch.setattr(settings, "memory_compressor_model", "test-compressor")
    monkeypatch.setattr(settings, "memory_extractor_model", "test-extractor")

    runtime = RuntimeLlmConfig(
        base_url="https://runtime.example/v1",
        api_key="runtime-key",
        model="runtime-model",
    )

    with patch("agent.agent.ChatOpenAI"), \
         patch("agent.agent.create_react_agent"), \
         patch("memory.memory_manager.SessionCompressor") as mock_compressor, \
         patch("memory.memory_manager.KnowledgeExtractor") as mock_extractor, \
         patch("memory.memory_manager.VectorStore"):
        AIAgent(llm_config=runtime)

    mock_compressor.assert_called_with(
        model="runtime-model",
        base_url="https://runtime.example/v1",
        api_key="runtime-key",
    )
    mock_extractor.assert_called_with(
        model="runtime-model",
        base_url="https://runtime.example/v1",
        api_key="runtime-key",
    )


def test_agent_memory_initialization_disabled(monkeypatch):
    """When memory is disabled in settings, AIAgent should have memory_manager set to None."""
    monkeypatch.setattr(settings, "memory_enabled", False)

    with patch("agent.agent.ChatOpenAI"), patch("agent.agent.create_react_agent"):
        agent = AIAgent()
        assert agent.memory_manager is None


def test_chat_sync_endpoint_memory_integration(monkeypatch):
    """Verify sync chat reads memory before execution and commits stable memory after response."""
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    monkeypatch.setattr(settings, "memory_enabled", True)
    
    dummy_chat_id = "test-chat-sync-123"
    dummy_message = "测试徒步路线"
    
    mock_memory_ctx = {
        "session_context": "Previous route discussed: Route A",
        "knowledge_context": "## 已知的用户信息\n- 喜欢徒步"
    }

    # Patch ChatOpenAI, react agent creation, and memory read/commit.
    with patch("agent.agent.ChatOpenAI"), \
         patch("agent.agent.create_react_agent") as mock_create_agent, \
         patch("memory.MemoryManager.build_runtime_context", return_value=mock_memory_ctx) as mock_read, \
         patch("memory.MemoryManager.commit_interaction", return_value=1) as mock_commit:
        
        # Mock the react agent's ainvoke method to return a dummy response
        mock_agent_instance = MagicMock()
        async def mock_ainvoke(*args, **kwargs):
            return {"messages": [MagicMock(content="Mocked Sync Response")]}
        mock_agent_instance.ainvoke = mock_ainvoke
        mock_create_agent.return_value = mock_agent_instance

        client = TestClient(app)
        response = client.post(
            "/api/v1/chat/sync",
            json={"chat_id": dummy_chat_id, "message": dummy_message}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Mocked Sync Response"
        assert data["chat_id"] == dummy_chat_id

        # Runtime context is read-only before execution.
        mock_read.assert_called_once()
        args, kwargs = mock_read.call_args
        assert args[1] == dummy_message
        mock_commit.assert_called_once()
        commit_args, _ = mock_commit.call_args
        assert commit_args[1] == dummy_message
        assert commit_args[2] == "Mocked Sync Response"
        assert all(value is None for value in commit_args[3]["slots"].values())


def test_chat_sse_endpoint_memory_integration(monkeypatch):
    """Verify SSE chat reads memory, streams properly, then commits memory."""
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    monkeypatch.setattr(settings, "memory_enabled", True)

    dummy_chat_id = "test-chat-sse-123"
    dummy_message = "测试流式响应"
    mock_memory_ctx = {
        "session_context": "Session Summary A",
        "knowledge_context": "## 已知的用户信息\n- User likes hiking"
    }

    with patch("agent.agent.ChatOpenAI"), \
         patch("agent.agent.create_react_agent") as mock_create_agent, \
         patch("memory.MemoryManager.build_runtime_context", return_value=mock_memory_ctx) as mock_read, \
         patch("memory.MemoryManager.commit_interaction", return_value=1) as mock_commit:

        # Mock the react agent's ainvoke method
        mock_agent_instance = MagicMock()
        async def mock_ainvoke(*args, **kwargs):
            return {"messages": [MagicMock(content="Mocked SSE Response")]}
        mock_agent_instance.ainvoke = mock_ainvoke
        mock_create_agent.return_value = mock_agent_instance

        client = TestClient(app)
        response = client.post(
            "/api/v1/chat/sse",
            json={"chat_id": dummy_chat_id, "message": dummy_message}
        )

        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        # Read the event stream chunks
        lines = [line if isinstance(line, str) else line.decode("utf-8") for line in response.iter_lines() if line]
        events = []
        for line in lines:
            if line.startswith("data: "):
                events.append(json.loads(line[6:]))

        assert len(events) > 0
        # The last event or one of the events should return the final text
        text_events = [e for e in events if e.get("type") == "text"]
        assert len(text_events) > 0
        assert text_events[0]["content"] == "Mocked SSE Response"

        mock_read.assert_called_once()
        mock_commit.assert_called_once()


def test_chat_memory_disabled_no_calls(monkeypatch):
    """When memory is disabled, MemoryManager should not be called."""
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    monkeypatch.setattr(settings, "memory_enabled", False)

    dummy_chat_id = "test-chat-disabled"
    dummy_message = "测试内存关闭"

    with patch("agent.agent.ChatOpenAI"), \
         patch("agent.agent.create_react_agent") as mock_create_agent, \
         patch("memory.MemoryManager.build_runtime_context") as mock_read, \
         patch("memory.MemoryManager.commit_interaction") as mock_commit:

        mock_agent_instance = MagicMock()
        async def mock_ainvoke(*args, **kwargs):
            return {"messages": [MagicMock(content="Mocked Disabled Response")]}
        mock_agent_instance.ainvoke = mock_ainvoke
        mock_create_agent.return_value = mock_agent_instance

        client = TestClient(app)
        response = client.post(
            "/api/v1/chat/sync",
            json={"chat_id": dummy_chat_id, "message": dummy_message}
        )

        assert response.status_code == 200
        assert response.json()["content"] == "Mocked Disabled Response"

        mock_read.assert_not_called()
        mock_commit.assert_not_called()


def test_chat_memory_exception_fallback(monkeypatch):
    """When MemoryManager raises an exception, the agent should catch it gracefully and proceed."""
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    monkeypatch.setattr(settings, "memory_enabled", True)

    dummy_chat_id = "test-chat-error"
    dummy_message = "测试内存报错 fallback"

    with patch("agent.agent.ChatOpenAI"), \
         patch("agent.agent.create_react_agent") as mock_create_agent, \
         patch("memory.MemoryManager.build_runtime_context", side_effect=RuntimeError("VectorDB Connection Failed")) as mock_read, \
         patch("memory.MemoryManager.commit_interaction", return_value=1) as mock_commit:

        mock_agent_instance = MagicMock()
        async def mock_ainvoke(*args, **kwargs):
            return {"messages": [MagicMock(content="Mocked Recovery Response")]}
        mock_agent_instance.ainvoke = mock_ainvoke
        mock_create_agent.return_value = mock_agent_instance

        client = TestClient(app)
        # Even with memory failure, the API call should succeed with HTTP 200
        response = client.post(
            "/api/v1/chat/sync",
            json={"chat_id": dummy_chat_id, "message": dummy_message}
        )

        assert response.status_code == 200
        assert response.json()["content"] == "Mocked Recovery Response"
        mock_read.assert_called_once()
        mock_commit.assert_called_once()
