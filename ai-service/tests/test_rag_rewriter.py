"""Tests for RAG QueryRewriter — semantic rewrite via LangChain."""

import os
import sys
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.documents import Document


def test_rewriter_returns_list_of_strings():
    """QueryRewriter.rewrite must return list[str]."""
    from rag.rewriter import QueryRewriter

    rewriter = QueryRewriter()
    result = rewriter.rewrite("徒步安全")
    assert isinstance(result, list)
    assert all(isinstance(q, str) for q in result)


def test_rewriter_includes_original_question():
    """First element must be the original question."""
    from rag.rewriter import QueryRewriter

    rewriter = QueryRewriter()
    result = rewriter.rewrite("徒步安全")
    assert result[0] == "徒步安全"


def test_rewriter_fallback_without_llm():
    """Without LLM config, rewriter should fallback to template-based rewrite."""
    from rag.rewriter import QueryRewriter

    rewriter = QueryRewriter()  # no api_key → no LLM
    result = rewriter.rewrite("登山装备")
    assert len(result) >= 2  # original + at least 1 variation
    assert "登山装备" in result[0]


def test_rewriter_semantic_with_llm(monkeypatch):
    """With LLM configured, rewriter uses ChatModel for semantic rewrite."""
    from rag.rewriter import QueryRewriter

    class FakeAIMessage:
        content = '["登山需要什么装备", "户外徒步装备清单", "登山安全注意事项"]'

    class FakeChatModel:
        def invoke(self, messages):
            return FakeAIMessage()

    monkeypatch.setattr("rag.rewriter.ChatOpenAI", lambda **kw: FakeChatModel())

    rewriter = QueryRewriter(api_key="test-key", base_url="http://fake", model="test")
    result = rewriter.rewrite("登山装备")

    assert len(result) >= 2
    assert "登山装备" in result[0]  # original always first
    # Semantic variations should differ from template
    assert "登山需要什么装备" in result or "户外徒步装备清单" in result


def test_rewriter_contextualizes_follow_up_with_history():
    """Pronoun-like follow-up questions should become standalone retrieval queries."""
    from rag.rewriter import QueryRewriter

    rewriter = QueryRewriter(api_key="", base_url="", model="")
    result = rewriter.contextualize(
        "如果是雨天，这些装备需要怎么调整？",
        [{"role": "user", "content": "户外徒步需要准备什么装备"}],
    )

    assert result == "针对户外徒步需要准备什么装备，如果是雨天，这些装备需要怎么调整？"


def test_rewriter_contextualizes_short_follow_up_particle():
    """Short follow-ups like '装备呢' should keep their prior topic."""
    from rag.rewriter import QueryRewriter

    rewriter = QueryRewriter(api_key="", base_url="", model="")
    result = rewriter.contextualize(
        "装备呢？",
        [{"role": "user", "content": "户外徒步需要准备什么"}],
    )

    assert result == "针对户外徒步需要准备什么，装备呢？"
