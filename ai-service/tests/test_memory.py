"""Tests for the two-level memory system (L1 session compression + L2 knowledge extraction)."""

import json
import sys
import os
import re

import numpy as np
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ensure OPENAI_API_KEY is set (config.py requires it on import)
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = "test-key-for-testing"


# ── Cycle 1: SessionCompressor (L1) ──────────────────────────────────


class TestSessionCompressor:
    """Verify L1 session compression logic: LLM path, fallback path, edge cases."""

    @pytest.fixture(autouse=True)
    def _mock_llm(self):
        """Default: mock ChatOpenAI so no real API call is made."""
        patcher = patch("memory.compressor.ChatOpenAI")
        mock_cls = patcher.start()
        self.mock_llm_instance = MagicMock()
        mock_cls.return_value = self.mock_llm_instance
        yield
        patcher.stop()

    # ── imports after patching ──

    @pytest.fixture(autouse=True)
    def _imports(self):
        from memory.compressor import SessionCompressor

        self.SessionCompressor = SessionCompressor

    # ── tests ──

    def test_compress_empty_history_returns_empty_string(self):
        """Empty history list returns empty string."""
        compressor = self.SessionCompressor()
        assert compressor.compress([]) == ""

    def test_compress_no_dialogue_messages_returns_empty(self):
        """Only system messages (no user/assistant) returns empty string."""
        compressor = self.SessionCompressor()
        history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "Use Chinese."},
        ]
        assert compressor.compress(history) == ""

    def test_fallback_used_when_llm_raises(self):
        """When ChatOpenAI.invoke raises, fallback compression is used."""
        self.mock_llm_instance.invoke.side_effect = RuntimeError("API unavailable")
        compressor = self.SessionCompressor()

        history = [
            {"role": "user", "content": "今天的天气怎么样？"},
            {"role": "assistant", "content": "今天天气晴朗，气温25度。"},
        ]
        result = compressor.compress(history)
        assert "初始提问" in result
        assert "总消息数" in result

    def test_fallback_contains_expected_fields(self):
        """Fallback output includes initial question, recent dialogue, and message count."""
        self.mock_llm_instance.invoke.side_effect = RuntimeError("fail")
        compressor = self.SessionCompressor()

        history = [
            {"role": "user", "content": "帮我写一封邮件"},
            {"role": "assistant", "content": "好的，请提供收件人和主题。"},
            {"role": "user", "content": "发给张总，关于项目进度"},
            {"role": "assistant", "content": "邮件内容已准备好。"},
        ]
        result = compressor.compress(history)
        assert "初始提问" in result
        assert "最近对话" in result
        assert "总消息数: 4" in result

    def test_llm_success_returns_llm_output(self):
        """When LLM succeeds, its output is returned as the compressed summary."""
        self.mock_llm_instance.invoke.return_value = MagicMock(
            content="用户询问天气，助手回答晴天25度。"
        )
        compressor = self.SessionCompressor()

        history = [
            {"role": "user", "content": "今天天气怎么样？"},
            {"role": "assistant", "content": "今天天气晴朗，气温25度。"},
        ]
        result = compressor.compress(history)
        assert result == "用户询问天气，助手回答晴天25度。"

    def test_llm_empty_content_falls_back(self):
        """When LLM returns empty content, fallback is used."""
        self.mock_llm_instance.invoke.return_value = MagicMock(content="")
        compressor = self.SessionCompressor()

        history = [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ]
        result = compressor.compress(history)
        assert "初始提问" in result

    def test_single_message_handled(self):
        """A single user message still produces a fallback summary."""
        self.mock_llm_instance.invoke.side_effect = RuntimeError("fail")
        compressor = self.SessionCompressor()

        history = [{"role": "user", "content": "你是谁？"}]
        result = compressor.compress(history)
        assert "初始提问: 你是谁？" in result
        assert "总消息数: 1" in result

    def test_llm_called_with_correct_prompt(self):
        """Verify ChatOpenAI.invoke is called with a SystemMessage + HumanMessage."""
        compressor = self.SessionCompressor()
        history = [
            {"role": "user", "content": "test"},
            {"role": "assistant", "content": "response"},
        ]
        compressor.compress(history)
        assert self.mock_llm_instance.invoke.called
        args, _ = self.mock_llm_instance.invoke.call_args
        messages = args[0]
        assert len(messages) == 2
        assert messages[0].type == "system"
        assert messages[1].type == "human"


# ── Cycle 2: KnowledgeExtractor (L2) ─────────────────────────────────


class TestKnowledgeExtractor:
    """Verify L2 knowledge extraction: LLM path, JSON parsing, edge cases."""

    @pytest.fixture(autouse=True)
    def _mock_llm(self):
        patcher = patch("memory.knowledge.ChatOpenAI")
        mock_cls = patcher.start()
        self.mock_llm_instance = MagicMock()
        mock_cls.return_value = self.mock_llm_instance
        yield
        patcher.stop()

    @pytest.fixture(autouse=True)
    def _imports(self):
        from memory.knowledge import KnowledgeExtractor

        self.KnowledgeExtractor = KnowledgeExtractor

    def test_extract_short_text_returns_empty(self):
        """Text shorter than 20 characters returns empty list."""
        extractor = self.KnowledgeExtractor()
        assert extractor.extract("你好") == []

    def test_extract_empty_text_returns_empty(self):
        """Empty string returns empty list."""
        extractor = self.KnowledgeExtractor()
        assert extractor.extract("") == []

    def test_extract_whitespace_text_returns_empty(self):
        """Whitespace-only text returns empty list."""
        extractor = self.KnowledgeExtractor()
        assert extractor.extract("   ") == []

    def test_extract_llm_failure_returns_empty(self):
        """When ChatOpenAI.invoke raises, returns empty list."""
        self.mock_llm_instance.invoke.side_effect = RuntimeError("API error")
        extractor = self.KnowledgeExtractor()
        result = extractor.extract("用户说他们喜欢编程，特别是Python语言。")
        assert result == []

    def test_extract_llm_success_parses_json(self):
        """When LLM returns valid JSON array, items are parsed correctly."""
        knowledge_json = json.dumps([
            {"type": "preference", "subject": "用户", "predicate": "喜欢", "object": "Python", "confidence": 0.9},
            {"type": "fact", "subject": "用户", "predicate": "使用", "object": "MacBook Pro", "confidence": 0.8},
        ])
        self.mock_llm_instance.invoke.return_value = MagicMock(content=knowledge_json)
        extractor = self.KnowledgeExtractor()
        result = extractor.extract("用户说他们喜欢编程，用MacBook Pro。")
        assert len(result) == 2
        assert result[0]["subject"] == "用户"
        assert result[0]["predicate"] == "喜欢"
        assert result[1]["object"] == "MacBook Pro"

    def test_extract_llm_markdown_wrapped_json(self):
        """LLM output wrapped in ```json ... ``` is parsed correctly."""
        markdown_wrapped = "```json\n[\n  {\"type\": \"fact\", \"subject\": \"用户\", \"predicate\": \"住在\", \"object\": \"北京\"}\n]\n```"
        self.mock_llm_instance.invoke.return_value = MagicMock(content=markdown_wrapped)
        extractor = self.KnowledgeExtractor()
        # Use a 20+ character input to pass the extract() length guard
        result = extractor.extract("你好，用户刚才说他自己住在北京，这是他的个人偏好。")
        assert len(result) == 1
        assert result[0]["object"] == "北京"

    def test_extract_invalid_json_returns_empty(self):
        """LLM returns non-JSON text → empty list (graceful degradation)."""
        self.mock_llm_instance.invoke.return_value = MagicMock(content="抱歉，我无法提取知识。")
        extractor = self.KnowledgeExtractor()
        result = extractor.extract("用户说了一些话。")
        assert result == []

    def test_parse_result_validates_required_fields(self):
        """Items without mandatory 'subject' or 'predicate' are filtered out."""
        from memory.knowledge import KnowledgeExtractor as KE

        raw = json.dumps([
            {"subject": "有效", "predicate": "是", "object": "有效项", "confidence": 0.9},
            {"object": "缺失subject和predicate", "confidence": 0.5},
            {"subject": "半有效", "object": "缺predicate", "confidence": 0.7},
        ])
        result = KE._parse_result(raw)
        assert len(result) == 1
        assert result[0]["subject"] == "有效"

    def test_parse_result_empty_content(self):
        """Empty content returns empty list."""
        from memory.knowledge import KnowledgeExtractor as KE

        assert KE._parse_result("") == []

    def test_parse_result_not_a_list(self):
        """LLM returns a dict instead of list → empty list."""
        from memory.knowledge import KnowledgeExtractor as KE

        assert KE._parse_result('{"type": "fact"}') == []


# ── Cycle 3: VectorStore ─────────────────────────────────────────────


class TestVectorStore:
    """Verify vector store: add/search/save/load/clear with mocked embeddings."""

    @pytest.fixture(autouse=True)
    def _mock_embeddings(self):
        """Mock OpenAIEmbeddings so no real API call is made."""
        patcher = patch("memory.vector_store.OpenAIEmbeddings")
        mock_cls = patcher.start()
        self.mock_emb_instance = MagicMock()
        mock_cls.return_value = self.mock_emb_instance
        yield
        patcher.stop()

    @pytest.fixture(autouse=True)
    def _imports(self, tmp_path, monkeypatch):
        import memory.vector_store as vector_store_module
        from memory.vector_store import VectorStore

        monkeypatch.setattr(vector_store_module.settings, "redis_url", "")
        monkeypatch.setattr(vector_store_module.settings, "redis_rest_url", "")
        monkeypatch.setattr(vector_store_module.settings, "redis_rest_token", "")

        self.VectorStore = VectorStore
        self.store_path = str(tmp_path / "memory_store")

    def make_store(self):
        """Helper: create a VectorStore with mocked embedding responses."""
        store = self.VectorStore(store_path=self.store_path)
        # Make sure _load doesn't interfere — empty store at start
        return store

    def _setup_mock_embeddings(self, store, num_items=3, dim=4):
        """Set up mock embeddings that return deterministic vectors."""
        # Generate deterministic vectors for documents
        doc_vectors = []
        for i in range(num_items):
            vec = [0.0] * dim
            vec[i % dim] = 1.0
            doc_vectors.append(vec)
        self.mock_emb_instance.embed_documents.return_value = doc_vectors
        # Query embedding: closest to item 0
        self.mock_emb_instance.embed_query.return_value = [1.0, 0.0, 0.0, 0.0]

        # For search we also need FAISS not to interfere — force in-memory
        store._index = None

        return doc_vectors

    def test_add_items_increases_count(self):
        """Adding items increases the store count."""
        store = self.make_store()
        self._setup_mock_embeddings(store, num_items=2)
        store.add([
            {"subject": "用户", "predicate": "喜欢", "object": "Python"},
            {"subject": "用户", "predicate": "使用", "object": "VSCode"},
        ])
        assert store.count == 2

    def test_add_empty_items_does_nothing(self):
        """Adding an empty list does not change count."""
        store = self.make_store()
        store.add([])
        assert store.count == 0

    def test_search_empty_store_returns_empty(self):
        """Searching an empty store returns empty list."""
        store = self.make_store()
        assert store.search("test") == []

    def test_search_returns_relevant_items(self):
        """Search returns items ordered by relevance (closest match first)."""
        store = self.make_store()
        self._setup_mock_embeddings(store, num_items=3)
        store.add([
            {"subject": "item_A", "predicate": "color", "object": "red"},
            {"subject": "item_B", "predicate": "color", "object": "blue"},
            {"subject": "item_C", "predicate": "color", "object": "green"},
        ])
        results = store.search("red related query", k=2)
        assert len(results) == 2
        # First result should be item_0 (closest to [1,0,0,0])
        assert results[0]["subject"] == "item_A"

    def test_search_respects_top_k(self):
        """Search returns at most k results."""
        store = self.make_store()
        self._setup_mock_embeddings(store, num_items=5)
        items = [
            {"subject": f"item_{i}", "predicate": "test", "object": f"val_{i}"}
            for i in range(5)
        ]
        store.add(items)
        results = store.search("query", k=3)
        assert len(results) == 3

    def test_embedding_failure_does_not_crash(self):
        """When embed_documents fails, add() logs warning and returns gracefully."""
        store = self.make_store()
        self.mock_emb_instance.embed_documents.side_effect = RuntimeError("API error")
        store.add([{"subject": "test", "predicate": "is", "object": "broken"}])
        assert store.count == 0

    def test_query_embedding_failure_returns_empty(self):
        """When embed_query fails, search() returns empty list."""
        store = self.make_store()
        # Add an item first (needs working embed_documents)
        self.mock_emb_instance.embed_documents.return_value = [[1.0] + [0.0] * (store._dimension - 1)]
        store.add([{"subject": "test", "predicate": "is", "object": "working"}])
        # Now break query embedding
        self.mock_emb_instance.embed_query.side_effect = RuntimeError("API error")
        results = store.search("query")
        assert results == []

    def test_clear_removes_all_items(self):
        """Clear removes all items and resets count to 0."""
        store = self.make_store()
        store._items = [{"subject": "test", "predicate": "is", "object": "temp"}]
        store._embeddings = [[1.0] + [0.0] * (store._dimension - 1)]
        store.clear()
        assert store.count == 0

    def test_save_and_load_roundtrip(self):
        """Save persists items, load restores them."""
        # Create store A → add items → save
        store_a = self.make_store()
        self.mock_emb_instance.embed_documents.return_value = [[1.0] + [0.0] * (store_a._dimension - 1)]
        store_a.add([{"subject": "persist", "predicate": "上", "object": "持久化"}])
        assert store_a.count == 1

        # Create store B (same path) → should auto-load
        # We need to NOT call _setup_mock_embeddings because _load reads pickle
        store_b = self.VectorStore(store_path=self.store_path)
        # The pickle was saved with the embedded vector, _load restores _items and _embeddings
        assert store_b.count == 1
        assert store_b._items[0]["subject"] == "persist"


# ── Cycle 4: MemoryManager (Integration) ────────────────────────────


class TestMemoryManager:
    """Verify MemoryManager orchestrates L1 + L2 correctly."""

    @pytest.fixture(autouse=True)
    def _mock_all(self):
        """Mock all three inner components to isolate orchestration logic."""
        patcher1 = patch("memory.memory_manager.SessionCompressor")
        patcher2 = patch("memory.memory_manager.KnowledgeExtractor")
        patcher3 = patch("memory.memory_manager.VectorStore")
        self.MockCompressor = patcher1.start()
        self.MockExtractor = patcher2.start()
        self.MockVectorStore = patcher3.start()

        # Instance mocks
        self.mock_compressor = MagicMock()
        self.mock_extractor = MagicMock()
        self.mock_vector_store = MagicMock()
        self.MockCompressor.return_value = self.mock_compressor
        self.MockExtractor.return_value = self.mock_extractor
        self.MockVectorStore.return_value = self.mock_vector_store

        yield
        patcher1.stop()
        patcher2.stop()
        patcher3.stop()

    @pytest.fixture(autouse=True)
    def _imports(self):
        from memory.memory_manager import MemoryManager, MemoryConfig

        self.MemoryManager = MemoryManager
        self.MemoryConfig = MemoryConfig

    def test_process_interaction_calls_update_and_returns_context(self):
        """process_interaction calls update_knowledge and returns both context strings."""
        self.mock_compressor.compress.return_value = "L1 session summary"
        self.mock_extractor.extract.return_value = [
            {"subject": "用户", "predicate": "喜欢", "object": "Python"},
        ]
        self.mock_vector_store.search.return_value = [
            {"subject": "用户", "predicate": "喜欢", "object": "JavaScript"},
        ]

        manager = self.MemoryManager()
        history = [{"role": "user", "content": "我喜欢Python"}]
        result = manager.process_interaction(history, "用户喜欢什么？")

        # update_knowledge was called (via self.mock_extractor.extract)
        self.mock_extractor.extract.assert_called_once()
        self.mock_vector_store.add.assert_called_once()

        # Compressor was called for session context
        self.mock_compressor.compress.assert_called_once_with(history)

        # Vector store was searched for knowledge context
        self.mock_vector_store.search.assert_called_once()

        # Returned context
        assert result["session_context"] == "L1 session summary"
        assert "已知的用户信息" in result["knowledge_context"]

    def test_get_session_context_delegates_to_compressor(self):
        """get_session_context calls compressor.compress."""
        self.mock_compressor.compress.return_value = "summary"
        manager = self.MemoryManager()
        history = [{"role": "user", "content": "hi"}]
        assert manager.get_session_context(history) == "summary"
        self.mock_compressor.compress.assert_called_with(history)

    def test_get_relevant_knowledge_delegates_to_vector_store(self):
        """get_relevant_knowledge calls vector_store.search."""
        self.mock_vector_store.search.return_value = [
            {"subject": "知识", "predicate": "是", "object": "力量"},
        ]
        manager = self.MemoryManager()
        result = manager.get_relevant_knowledge("test query")
        assert len(result) == 1
        self.mock_vector_store.search.assert_called_with("test query", k=5)

    def test_update_knowledge_empty_history(self):
        """update_knowledge with empty history returns 0 and calls nothing."""
        manager = self.MemoryManager()
        assert manager.update_knowledge([]) == 0
        self.mock_extractor.extract.assert_not_called()

    def test_update_knowledge_extracts_and_stores(self):
        """update_knowledge extracts from recent history and stores to vector store."""
        self.mock_extractor.extract.return_value = [
            {"subject": "用户", "predicate": "使用", "object": "Mac"},
        ]
        manager = self.MemoryManager()
        history = [
            {"role": "user", "content": "我用Mac电脑"},
            {"role": "assistant", "content": "好的，Mac很不错。"},
        ]
        count = manager.update_knowledge(history)
        assert count == 1
        self.mock_extractor.extract.assert_called_once()
        self.mock_vector_store.add.assert_called_once()

    def test_update_knowledge_only_user_assistant(self):
        """System messages are not passed to the extractor."""
        self.mock_extractor.extract.return_value = []
        manager = self.MemoryManager()
        history = [
            {"role": "system", "content": "You are a bot."},
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！"},
        ]
        manager.update_knowledge(history)
        # Verify extract was called with meaningful content, not system messages
        call_args = self.mock_extractor.extract.call_args[0][0]
        assert "You are a bot" not in call_args
        assert "你好" in call_args

    def test_format_knowledge_context_empty(self):
        """Format knowledge context returns empty string when no knowledge."""
        self.mock_vector_store.search.return_value = []
        manager = self.MemoryManager()
        assert manager.format_knowledge_context("query") == ""

    def test_format_knowledge_context_formats_items(self):
        """Format knowledge context produces readable bullet list."""
        self.mock_vector_store.search.return_value = [
            {"subject": "用户", "predicate": "喜欢", "object": "Python"},
            {"subject": "用户", "predicate": "使用", "object": "VSCode"},
        ]
        manager = self.MemoryManager()
        result = manager.format_knowledge_context("query")
        assert "已知的用户信息" in result
        assert "Python" in result
        assert "VSCode" in result
        assert result.startswith("##")

    def test_memory_config_defaults(self):
        """MemoryConfig has reasonable defaults."""
        config = self.MemoryConfig()
        assert config.compressor_model == "gpt-4o-mini"
        assert config.extractor_model == "gpt-4o-mini"
        assert config.top_k == 5

    def test_custom_config_used(self):
        """Custom MemoryConfig is passed to inner components."""
        config = self.MemoryConfig()
        config.compressor_model = "gpt-4o"
        config.vector_store_path = "/tmp/custom_store"

        manager = self.MemoryManager(config=config)

        # Compressor created with custom model
        self.MockCompressor.assert_called_with(model="gpt-4o", base_url="", api_key="")
        # VectorStore created with custom path
        self.MockVectorStore.assert_called_with(store_path="/tmp/custom_store")

    def test_runtime_llm_config_passed_to_memory_llm_components(self):
        """Memory compression/extraction should use request runtime LLM config when provided."""
        config = self.MemoryConfig(
            compressor_model="runtime-model",
            extractor_model="runtime-model",
            llm_base_url="https://runtime.example/v1",
            llm_api_key="runtime-key",
        )

        self.MemoryManager(config=config)

        self.MockCompressor.assert_called_with(
            model="runtime-model",
            base_url="https://runtime.example/v1",
            api_key="runtime-key",
        )
        self.MockExtractor.assert_called_with(
            model="runtime-model",
            base_url="https://runtime.example/v1",
            api_key="runtime-key",
        )
