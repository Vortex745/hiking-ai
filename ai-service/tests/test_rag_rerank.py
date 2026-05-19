"""Tests for RAG rerank integration."""

import json
import os
import sys
from pathlib import Path

from langchain_core.documents import Document

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app


def test_rag_query_reranks_documents_before_augmentation(monkeypatch):
    """RAG query should rerank retrieved chunks before building the final context."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        def similarity_search(self, query, k=2, status_filter=None):
            return [
                Document(page_content="低相关徒步内容", metadata={"source": "a"}),
                Document(page_content="高相关徒步内容", metadata={"source": "b"}),
            ]

    class FakeRewriter:
        def rewrite(self, question):
            return [question]

    class FakeReranker:
        @property
        def enabled(self):
            return True

        def rerank(self, query, docs):
            seen["input"] = [doc.page_content for doc in docs]
            return [
                Document(page_content="高相关徒步内容", metadata={"source": "b", "rerank_score": 0.98}),
                Document(page_content="低相关徒步内容", metadata={"source": "a", "rerank_score": 0.12}),
            ]

    class FakeAugmenter:
        def augment(self, question, docs):
            seen["augmented"] = [doc.page_content for doc in docs]
            return f"first={docs[0].page_content};score={docs[0].metadata['rerank_score']}"

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "徒步相关性"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["input"] == ["低相关徒步内容", "高相关徒步内容"]
    assert seen["augmented"] == ["高相关徒步内容", "低相关徒步内容"]
    assert "first=高相关徒步内容;score=0.98" in body
    assert "调用 Rerank 模型重排候选片段" in body


def test_rag_query_uses_hybrid_retrieval_and_humanized_question(monkeypatch):
    """RAG query should use hybrid retrieval, then humanize the generation query."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        storage_mode = "pgvector"

        def hybrid_search(self, queries, k=4, status_filter=None):
            seen["queries"] = queries
            seen["status_filter"] = status_filter
            return [
                Document(page_content="高海拔徒步先降低速度", metadata={"source": "guide"}),
            ]

    class FakeRewriter:
        def rewrite(self, question):
            return [question, "高海拔徒步节奏"]

        def humanize_for_answer(self, question):
            seen["humanize_input"] = question
            return "高海拔徒步怎么安排节奏？"

    class FakeReranker:
        @property
        def enabled(self):
            return False

    class FakeAugmenter:
        def augment(self, question, docs):
            seen["augment_question"] = question
            return f"answer for {question}: {docs[0].page_content}"

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "高反咋办"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["queries"] == ["高反咋办", "高海拔徒步节奏"]
    assert seen["humanize_input"] == "高反咋办"
    assert seen["augment_question"] == "高海拔徒步怎么安排节奏？"
    assert "LangChain 混合检索组件" in body
    assert "BM25 + RRF" in body
    assert "humanizer-zh" in body
    assert "answer for 高海拔徒步怎么安排节奏？" in body


def test_rag_query_passes_runtime_model_settings(monkeypatch):
    """RAG query should use model settings supplied by the frontend request."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        def __init__(self, **kwargs):
            seen["retriever"] = kwargs

        def similarity_search(self, query, k=2, status_filter=None):
            return [Document(page_content="runtime doc", metadata={"source": "runtime"})]

    class FakeRewriter:
        def __init__(self, **kwargs):
            seen["rewriter"] = kwargs

        def rewrite(self, question):
            return [question]

    class FakeReranker:
        def __init__(self, **kwargs):
            seen["reranker"] = kwargs

        @property
        def enabled(self):
            return False

        def rerank(self, query, docs):
            return docs

    class FakeAugmenter:
        def __init__(self, **kwargs):
            seen["augmenter"] = kwargs

        def augment(self, question, docs):
            return f"{question}:{docs[0].page_content}"

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)
    payload = {
        "question": "runtime config",
        "model_settings": {
            "llm": {
                "base_url": "https://chat.example/v1",
                "api_key": "chat-key",
                "model": "chat-model",
            },
            "embedding": {
                "base_url": "https://embed.example/v1",
                "api_key": "embedding-key",
                "model": "embed-model",
                "dimensions": 4096,
            },
            "rerank": {
                "base_url": "https://rerank.example/v1",
                "api_key": "rerank-key",
                "model": "rerank-model",
            },
        },
    }

    payload["question"] = "runtime doc"
    with client.stream("POST", "/api/v1/rag/query", json=payload) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert body
    assert seen["retriever"]["base_url"] == "https://embed.example/v1"
    assert seen["retriever"]["api_key"] == "embedding-key"
    assert seen["retriever"]["model"] == "embed-model"
    assert seen["retriever"]["dimensions"] == 4096
    assert seen["reranker"]["base_url"] == "https://rerank.example/v1"
    assert seen["reranker"]["api_key"] == "rerank-key"
    assert seen["reranker"]["model"] == "rerank-model"
    assert seen["augmenter"]["base_url"] == "https://chat.example/v1"
    assert seen["augmenter"]["api_key"] == "chat-key"
    assert seen["augmenter"]["model"] == "chat-model"


def test_rag_query_retries_default_embedding_when_runtime_embedding_returns_empty(monkeypatch):
    """Bad runtime embedding settings should fall back to default RAG retrieval."""

    from api import rag as rag_api

    seen = {"retrievers": []}

    class FakeRetriever:
        storage_mode = "pgvector"

        def __init__(self, **kwargs):
            self.kwargs = kwargs
            seen["retrievers"].append(kwargs)

        def hybrid_search(self, queries, k=4, status_filter=None):
            if self.kwargs:
                return []
            return [
                Document(
                    page_content="徒步的核心目的在于亲近自然、挑战自我、提升身心素质。",
                    metadata={"source": "feishu", "title": "户外徒步知识文档.md"},
                )
            ]

    class FakeRewriter:
        def __init__(self, **kwargs):
            pass

        def rewrite(self, question):
            return [question]

        def humanize_for_answer(self, question):
            return question

    class FakeReranker:
        def __init__(self, **kwargs):
            pass

        @property
        def enabled(self):
            return False

    class FakeAugmenter:
        def __init__(self, **kwargs):
            pass

        def augment(self, question, docs):
            return docs[0].page_content

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)
    payload = {
        "question": "徒步的核心目的",
        "model_settings": {
            "embedding": {
                "base_url": "https://bad-embedding.example/v1",
                "api_key": "bad-key",
                "model": "bad-embed",
                "dimensions": 4096,
            }
        },
    }

    with client.stream("POST", "/api/v1/rag/query", json=payload) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["retrievers"][0]["base_url"] == "https://bad-embedding.example/v1"
    assert seen["retrievers"][1] == {}
    assert "正在使用默认配置重试" in body
    assert "徒步的核心目的在于亲近自然" in body


def test_rag_query_emits_process_steps_and_document_summary(monkeypatch):
    """RAG query should stream structured process and document-search events."""

    from api import rag as rag_api

    class FakeRetriever:
        storage_mode = "memory"

        def similarity_search(self, query, k=2, status_filter=None):
            return [
                Document(
                    page_content="第一段知识库内容",
                    metadata={
                        "source": "feishu",
                        "title": "徒步安全手册",
                        "feishu_doc_token": "doc_token_1",
                    },
                ),
                Document(
                    page_content="第二段知识库内容",
                    metadata={
                        "source": "upload",
                        "title": "装备清单",
                        "file_name": "gear.md",
                    },
                ),
            ]

    class FakeRewriter:
        def rewrite(self, question):
            return [question]

    class FakeReranker:
        @property
        def enabled(self):
            return False

    class FakeAugmenter:
        def augment(self, question, docs):
            return "自然中文回答"

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "怎么安全徒步"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert '"type": "process"' in body
    assert "调用查询改写模块生成检索查询" in body
    assert "调用 embedding 模型生成查询向量" in body
    assert "使用向量在 pgvector/memory 中召回候选片段" in body
    assert "构造上下文并调用 LLM 生成回答" in body
    assert '"type": "documents"' in body
    assert '"searched_count": 2' in body
    assert '"matched_chunks": 2' in body
    assert "徒步安全手册" in body
    assert "第一段知识库内容" in body
    assert "自然中文回答" in body


def test_rag_upload_passes_runtime_embedding_settings(monkeypatch, tmp_path):
    """RAG upload should use frontend-supplied embedding settings for vector sync."""

    from api import rag as rag_api

    seen = {}

    class FakeLoader:
        def load_and_split(self, path):
            seen["path"] = path
            return [Document(page_content="uploaded doc", metadata={"source": path})]

    class FakeRetriever:
        def __init__(self, **kwargs):
            seen["retriever"] = kwargs

        def add_documents(self, docs, status=None):
            seen["docs"] = docs
            seen["status"] = status

    monkeypatch.setattr(rag_api, "RAG_DOCS_DIR", tmp_path)
    monkeypatch.setattr(rag_api, "DocumentLoader", FakeLoader)
    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)

    client = TestClient(app)
    runtime_settings = {
        "embedding": {
            "base_url": "https://embed.example/v1",
            "api_key": "embedding-key",
            "model": "embed-model",
            "dimensions": 4096,
        },
    }

    response = client.post(
        "/api/v1/rag/upload",
        files={"file": ("note.txt", b"hello", "text/plain")},
        data={
            "status": "feishu",
            "model_settings": json.dumps(runtime_settings),
        },
    )

    assert response.status_code == 200
    assert seen["retriever"]["base_url"] == "https://embed.example/v1"
    assert seen["retriever"]["api_key"] == "embedding-key"
    assert seen["retriever"]["model"] == "embed-model"
    assert seen["retriever"]["dimensions"] == 4096
    assert seen["status"] == "feishu"
