"""Tests for RAG VectorStoreRetriever — LangChain VectorStore abstraction."""

import os
import sys
from pathlib import Path

from langchain_core.documents import Document

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_retriever_add_and_search(monkeypatch):
    """VectorStoreRetriever should add docs and return relevant results."""
    from rag.retriever import VectorStoreRetriever

    class FakeEmbeddings:
        def embed_query(self, text):
            return [0.1] * 8

        def embed_documents(self, texts):
            return [[0.1] * 8 for _ in texts]

    monkeypatch.setattr("rag.retriever.OpenAIEmbeddings", lambda **kw: FakeEmbeddings())

    retriever = VectorStoreRetriever()
    docs = [
        Document(page_content="徒步安全指南", metadata={"source": "test"}),
        Document(page_content="登山装备清单", metadata={"source": "test"}),
    ]
    retriever.add_documents(docs)

    results = retriever.similarity_search("徒步", k=2)
    assert isinstance(results, list)
    # Should return documents (in-memory store with fake embeddings)
    assert len(results) <= 2


def test_retriever_storage_mode(monkeypatch):
    """VectorStoreRetriever should report correct storage_mode."""
    from rag.retriever import VectorStoreRetriever

    class FakeEmbeddings:
        def embed_query(self, text):
            return [0.1] * 8

        def embed_documents(self, texts):
            return [[0.1] * 8 for _ in texts]

    monkeypatch.setattr("rag.retriever.OpenAIEmbeddings", lambda **kw: FakeEmbeddings())

    retriever = VectorStoreRetriever()
    assert retriever.storage_mode in ("memory", "pgvector")


def test_retriever_no_dedup_in_add(monkeypatch):
    """Adding same doc twice should not crash (dedup handled at query level)."""
    from rag.retriever import VectorStoreRetriever

    class FakeEmbeddings:
        def embed_query(self, text):
            return [0.1] * 8

        def embed_documents(self, texts):
            return [[0.1] * 8 for _ in texts]

    monkeypatch.setattr("rag.retriever.OpenAIEmbeddings", lambda **kw: FakeEmbeddings())

    retriever = VectorStoreRetriever()
    doc = Document(page_content="重复内容", metadata={"source": "test"})
    retriever.add_documents([doc])
    retriever.add_documents([doc])  # should not raise

    results = retriever.similarity_search("重复", k=5)
    assert isinstance(results, list)


def test_hybrid_search_uses_bm25_and_rrf_when_vector_order_is_weak(monkeypatch):
    """Hybrid search should combine vector candidates with lexical BM25 via RRF."""
    from langchain_core.vectorstores import InMemoryVectorStore
    from rag.retriever import VectorStoreRetriever

    class FakeEmbeddings:
        def embed_query(self, text):
            return [0.1] * 8

        def embed_documents(self, texts):
            return [[0.1] * 8 for _ in texts]

    def force_memory_store(self):
        self._pg_client = None
        self._fallback_mode = True
        self._store = InMemoryVectorStore(embedding=self.embeddings)

    monkeypatch.setattr("rag.retriever.OpenAIEmbeddings", lambda **kw: FakeEmbeddings())
    monkeypatch.setattr(VectorStoreRetriever, "_try_connect_pgvector", force_memory_store)

    retriever = VectorStoreRetriever()
    docs = [
        Document(page_content="营地选择需要避开低洼地", metadata={"source": "camp"}),
        Document(page_content="炉具燃料要远离帐篷并保持通风", metadata={"source": "stove"}),
    ]
    retriever.add_documents(docs)

    results = retriever.hybrid_search(["炉具安全"], k=2)

    assert [doc.metadata["source"] for doc in results][:1] == ["stove"]
    assert results[0].metadata["retrieval_method"] == "hybrid_rrf"


def test_memory_fallback_documents_survive_new_retriever_instance():
    """Uploaded docs should remain queryable when memory fallback creates a new retriever."""
    from rag import retriever as retriever_module
    from rag.retriever import VectorStoreRetriever

    if hasattr(retriever_module, "_SHARED_FALLBACK_DOCS"):
        retriever_module._SHARED_FALLBACK_DOCS.clear()

    upload_retriever = VectorStoreRetriever(api_key="")
    upload_retriever.add_documents([
        Document(
            page_content="营地选择要避开低洼地，优先选择排水良好的平整区域。",
            metadata={"source": "upload", "status": "upload"},
        )
    ])

    query_retriever = VectorStoreRetriever(api_key="")
    results = query_retriever.hybrid_search(["营地 低洼地"], k=2, status_filter="upload")

    assert results
    assert "低洼地" in results[0].page_content
