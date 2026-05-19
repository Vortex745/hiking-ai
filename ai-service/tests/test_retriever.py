"""Tests for RAG vector retrieval behavior."""

import json
import os
import sys
from pathlib import Path

from langchain_core.documents import Document

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag import retriever as retriever_module


class _EmbeddingShouldNotRun:
    calls = 0

    def embed_query(self, query: str):
        self.calls += 1
        raise AssertionError("embedding API should not be called for an empty vector store")


class _EmptyPGClient:
    def __init__(self):
        self.status_filter = None

    def has_documents(self, status_filter=None):
        self.status_filter = status_filter
        return False

    def similarity_search(self, *args, **kwargs):
        raise AssertionError("pgvector search should not run when status filter is empty")


class _RecordingConnection:
    def __init__(self):
        self.calls = []
        self.closed = False

    def execute(self, sql, params=None):
        self.calls.append((sql, params))
        return self

    def fetchall(self):
        return [("doc-1", "same dimension doc", {"source": "test"}, 0.99)]


def test_pgvector_empty_status_filter_returns_without_embedding():
    """Empty pgvector results should not trigger embedding API calls."""

    embeddings = _EmbeddingShouldNotRun()
    pg_client = _EmptyPGClient()
    retriever = object.__new__(retriever_module.VectorStoreRetriever)
    retriever.embeddings = embeddings
    retriever._fallback_mode = False
    retriever._pg_client = pg_client
    retriever._store = None
    retriever._fallback_docs = []

    assert retriever.storage_mode == "pgvector"
    assert retriever.similarity_search("anything", status_filter="feishu") == []
    assert embeddings.calls == 0
    assert pg_client.status_filter == "feishu"


def test_pgvector_similarity_search_filters_to_query_dimensions():
    """Mixed-dimension pgvector rows should not break configured RAG retrieval."""

    client = object.__new__(retriever_module._PGVectorClient)
    conn = _RecordingConnection()
    client._conn = conn

    query_embedding = [0.1, 0.2, 0.3]
    rows = client.similarity_search(query_embedding, k=2)

    sql, params = conn.calls[-1]
    assert "vector_dims(embedding) = %s" in " ".join(sql.split())
    assert params[0] == json.dumps(query_embedding)
    assert params[1] == len(query_embedding)
    assert params[2] == json.dumps(query_embedding)
    assert params[3] == 2
    assert rows == [("doc-1", "same dimension doc", {"source": "test"}, 0.99)]


def test_hybrid_search_keeps_bm25_when_pgvector_embedding_fails():
    """Lexical retrieval should survive a runtime embedding provider failure."""

    class FailingEmbeddings:
        def embed_query(self, query):
            raise RuntimeError("embedding provider rejected request")

    class SearchFailingPGClient:
        def has_documents(self, status_filter=None):
            return True

        def similarity_search(self, query_embedding, k=4):
            raise AssertionError("query embedding should fail before pgvector search")

        def list_documents(self, status_filter=None):
            return [
                Document(
                    page_content="徒步的核心目的在于亲近自然、挑战自我、提升身心素质。",
                    metadata={"source": "feishu", "status": "feishu"},
                )
            ]

    retriever = object.__new__(retriever_module.VectorStoreRetriever)
    retriever.embeddings = FailingEmbeddings()
    retriever._fallback_mode = False
    retriever._pg_client = SearchFailingPGClient()
    retriever._store = None
    retriever._fallback_docs = []

    results = retriever.hybrid_search(["徒步的核心目的"], k=4, status_filter="feishu")

    assert len(results) == 1
    assert "核心目的" in results[0].page_content
    assert results[0].metadata["retrieval_method"] == "hybrid_rrf"
