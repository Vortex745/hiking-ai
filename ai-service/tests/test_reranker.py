"""Tests for RAG reranker behavior."""

import os
import sys
from pathlib import Path

from langchain_core.documents import Document

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.reranker import Reranker


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _Client:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append({"url": url, **kwargs})
        return _Response(self.payload)


def test_reranker_orders_documents_and_writes_scores():
    client = _Client({
        "results": [
            {"index": 1, "relevance_score": 0.91},
            {"index": 0, "relevance_score": 0.22},
        ],
    })
    docs = [
        Document(page_content="less relevant", metadata={"source": "a"}),
        Document(page_content="more relevant", metadata={"source": "b"}),
    ]

    reranker = Reranker(
        base_url="https://rerank.example/v1",
        api_key="rerank-key",
        model="rerank-model",
        top_k=2,
        enabled=True,
        client=client,
    )

    results = reranker.rerank("query", docs)

    assert [doc.page_content for doc in results] == ["more relevant", "less relevant"]
    assert results[0].metadata["rerank_score"] == 0.91
    assert results[0].metadata["rerank_rank"] == 1
    assert client.calls[0]["url"] == "https://rerank.example/v1/rerank"
    assert client.calls[0]["json"]["documents"] == ["less relevant", "more relevant"]


def test_reranker_disabled_returns_original_documents():
    docs = [
        Document(page_content="a"),
        Document(page_content="b"),
    ]
    reranker = Reranker(base_url="", api_key="", model="", enabled=True)

    assert reranker.rerank("query", docs) == docs
