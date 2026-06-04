"""Tests for RAG document retrieval and output generation."""

import json
import os
import sys
from pathlib import Path

from langchain_core.documents import Document

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app


def test_document_search_summary_uses_plain_text_preview():
    """Document preview should not expose markdown syntax in the chat UI."""

    from api.rag import summarize_retrieved_documents

    docs = [
        Document(
            page_content="# 户外徒步知识全指南\n\n徒步的主要目的是**亲近自然**、挑战自我。[1]",
            metadata={"source": "upload", "title": "户外徒步知识文档.md"},
        )
    ]

    summary = summarize_retrieved_documents(docs)
    preview = summary["documents"][0]["content"]

    assert preview == "户外徒步知识全指南 徒步的主要目的是亲近自然、挑战自我。"
    assert "**" not in preview
    assert "#" not in preview
    assert "[1]" not in preview


def test_rag_documents_lists_indexed_pgvector_documents(monkeypatch):
    from api import rag as rag_api

    class FakeRetriever:
        storage_mode = "pgvector"

        def document_count(self):
            return 2

        def indexed_documents(self):
            return [
                Document(page_content="chunk one", metadata={"title": "云知识库", "status": "cloud_docs"}),
                Document(page_content="chunk two", metadata={"title": "云知识库", "status": "cloud_docs"}),
            ]

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)

    client = TestClient(app)
    response = client.get("/api/v1/rag/documents")

    assert response.status_code == 200
    assert response.json()["documents"] == [
        {
            "id": response.json()["documents"][0]["id"],
            "filename": "云知识库",
            "status": "cloud_docs",
            "chunk_count": 2,
        }
    ]


def test_rag_health_counts_indexed_documents_not_tmp_files(monkeypatch, tmp_path):
    from api import rag as rag_api

    class FakeRetriever:
        storage_mode = "pgvector"

        def document_count(self):
            return 7

    monkeypatch.setattr(rag_api, "RAG_DOCS_DIR", tmp_path)
    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    (tmp_path / "ephemeral.md").write_text("tmp", encoding="utf-8")

    client = TestClient(app)
    response = client.get("/api/v1/rag/health")

    assert response.status_code == 200
    assert response.json()["documents"] == 7
    assert "memory" in response.json()


def test_rag_retrieves_documents_and_generates_answer(monkeypatch):
    """RAG query should retrieve relevant documents and produce an augmented answer."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        storage_mode = "memory"

        def similarity_search(self, query, k=2, status_filter=None):
            seen["search_query"] = query
            return [
                Document(
                    page_content="徒步时应携带足够的水和食物，注意天气变化。",
                    metadata={
                        "source": "upload",
                        "title": "徒步安全指南",
                        "file_name": "hiking_guide.md",
                    },
                ),
                Document(
                    page_content="建议穿着防滑登山鞋，携带急救包。",
                    metadata={
                        "source": "upload",
                        "title": "装备清单",
                        "file_name": "gear.md",
                    },
                ),
            ]

    class FakeRewriter:
        def rewrite(self, question):
            seen["rewritten"] = question
            return [question]

    class FakeReranker:
        @property
        def enabled(self):
            return False

    class FakeAugmenter:
        def augment(self, question, docs):
            seen["augmented_docs"] = [doc.page_content for doc in docs]
            seen["augmented_question"] = question
            return "根据徒步安全指南，建议携带足够的水、食物、防滑登山鞋和急救包，并注意天气变化。"

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "徒步需要准备什么"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200

    assert seen["search_query"] == "徒步需要准备什么"
    assert seen["rewritten"] == "徒步需要准备什么"

    assert len(seen["augmented_docs"]) == 2
    assert "徒步时应携带足够的水和食物" in seen["augmented_docs"][0]
    assert "防滑登山鞋" in seen["augmented_docs"][1]
    assert seen["augmented_question"] == "徒步需要准备什么"

    assert '"type": "documents"' in body
    assert '"searched_count": 2' in body
    assert '"matched_chunks": 2' in body
    assert "徒步安全指南" in body
    assert "装备清单" in body

    assert '"type": "text"' in body
    assert "根据徒步安全指南" in body
    assert "防滑登山鞋和急救包" in body

    assert '"type": "done"' in body


def test_rag_no_documents_returns_friendly_message(monkeypatch):
    """RAG query with no matching documents should return a friendly no-docs message."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        storage_mode = "memory"

        def similarity_search(self, query, k=2, status_filter=None):
            return []

    class FakeRewriter:
        def rewrite(self, question):
            return [question]

    class FakeReranker:
        @property
        def enabled(self):
            return False

    class FakeAugmenter:
        def augment(self, question, docs):
            seen["docs"] = docs
            return "我没在知识库里找到和「未知问题」直接相关的文档。"

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "量子物理是什么"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["docs"] == []
    assert '"type": "documents"' in body
    assert '"searched_count": 0' in body
    assert '"matched_chunks": 0' in body
    assert "我没在知识库里找到" in body
    assert '"type": "done"' in body


def test_rag_query_persists_messages_when_chat_id_is_provided(monkeypatch):
    from api import rag as rag_api

    persisted = []

    class FakeMemory:
        def add_message(self, role, content):
            persisted.append({"role": role, "content": content})

        def get_messages(self):
            return persisted

    monkeypatch.setattr(rag_api, "get_chat_memory", lambda chat_id: FakeMemory())

    client = TestClient(app)

    with client.stream(
        "POST",
        "/api/v1/rag/query",
        json={"question": "你好", "chat_id": "rag-persist"},
    ) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert '"type": "done"' in body
    assert persisted == [
        {"role": "user", "content": "你好"},
        {
            "role": "assistant",
            "content": "你好，我是 AI Hiking 的 RAG 助手。你可以上传文档后向我提问，也可以先问一些简单问题。",
        },
    ]


def test_rag_history_reads_persisted_messages(monkeypatch):
    from api import rag as rag_api

    class FakeMemory:
        def get_messages(self):
            return [{"role": "user", "content": "查知识库"}]

    monkeypatch.setattr(rag_api, "get_chat_memory", lambda chat_id: FakeMemory())

    client = TestClient(app)
    response = client.get("/api/v1/rag/history/rag-history")

    assert response.status_code == 200
    assert response.json() == {
        "chat_id": "rag-history",
        "messages": [{"role": "user", "content": "查知识库"}],
    }


def test_rag_query_syncs_cloud_docs_when_configured(monkeypatch):
    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        storage_mode = "memory"

        def add_documents(self, docs, status=None):
            seen["added_docs"] = docs
            seen["added_status"] = status

        def similarity_search(self, query, k=2, status_filter=None):
            return []

    class FakeCloudLoader:
        def load_and_split(self, api_url):
            seen["api_url"] = api_url
            return [
                Document(
                    page_content="云知识库：雷雨天气不要进入裸露山脊。",
                    metadata={"source": "cloud_docs", "title": "安全知识库"},
                )
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
            seen["augmented_docs"] = docs
            return f"已读取云知识库：{docs[0].page_content}"

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api.settings, "rag_docs_api_url", "http://api.example.com/docs/all")
    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "CloudDocsLoader", FakeCloudLoader)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "查知识库里的雷雨徒步"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["api_url"] == "http://api.example.com/docs/all"
    assert seen["added_status"] == "cloud_docs"
    assert seen["augmented_docs"][0].metadata["title"] == "安全知识库"
    assert "已同步云知识库文档" in body
    assert "雷雨天气不要进入裸露山脊" in body


def test_rag_query_syncs_feishu_link_before_retrieval(monkeypatch):
    """A Feishu link in the question should be synced into the immediate RAG answer."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        storage_mode = "memory"

        def add_documents(self, docs, status=None):
            seen["added_docs"] = docs
            seen["added_status"] = status

        def hybrid_search(self, queries, k=4, status_filter=None):
            return []

    class FakeLoader:
        def load_and_split(self, raw, doc_type="docx"):
            seen["link"] = raw
            seen["doc_type"] = doc_type
            return [
                Document(
                    page_content="营地要平坦、避风，距离水源60到200米，避开低洼地和枯树。",
                    metadata={"source": "feishu", "title": "营地选择指南"},
                )
            ]

    class FakeRewriter:
        def rewrite(self, question):
            return [question]

        def humanize_for_answer(self, question):
            return "这篇飞书文档讲了什么？"

    class FakeReranker:
        @property
        def enabled(self):
            return False

    class FakeAugmenter:
        def augment(self, question, docs):
            seen["augmented_docs"] = docs
            return f"已读取飞书：{docs[0].page_content}"

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api.settings, "rag_docs_api_url", "")
    monkeypatch.setattr(rag_api.settings, "feishu_app_id", "app-id")
    monkeypatch.setattr(rag_api.settings, "feishu_app_secret", "app-secret")
    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "FeishuDocLoader", FakeLoader)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)
    question = "阅读这篇文章告诉我内容 https://example.feishu.cn/docx/UHfYdYAuPoZDo8xxeOOc9g2Znpd"

    with client.stream("POST", "/api/v1/rag/query", json={"question": question}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["link"].endswith("UHfYdYAuPoZDo8xxeOOc9g2Znpd")
    assert seen["doc_type"] == "docx"
    assert seen["added_status"] == "feishu"
    assert seen["augmented_docs"][0].metadata["title"] == "营地选择指南"
    assert "检测到飞书链接" in body
    assert "已同步飞书文档" in body
    assert "营地要平坦、避风" in body


def test_rag_query_stops_when_feishu_link_sync_fails(monkeypatch):
    """Failed Feishu link sync should not be answered with unrelated knowledge docs."""

    from api import rag as rag_api

    class FakeRetriever:
        storage_mode = "memory"

    class FakeLoader:
        def load_and_split(self, raw, doc_type="docx"):
            raise RuntimeError("permission denied")

    async def no_sleep(*_args, **_kwargs):
        return None

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("RAG generation should not run after Feishu sync failure")

    monkeypatch.setattr(rag_api.settings, "rag_docs_api_url", "")
    monkeypatch.setattr(rag_api.settings, "feishu_app_id", "app-id")
    monkeypatch.setattr(rag_api.settings, "feishu_app_secret", "app-secret")
    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "FeishuDocLoader", FakeLoader)
    monkeypatch.setattr(rag_api, "QueryRewriter", fail_if_called)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)
    question = "阅读这篇文章告诉我内容 https://example.feishu.cn/docx/UHfYdYAuPoZDo8xxeOOc9g2Znpd"

    with client.stream("POST", "/api/v1/rag/query", json={"question": question}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert "检测到飞书链接" in body
    assert "没有同步到可检索的文档内容" in body
    assert "调用查询改写模块" not in body


def test_rag_query_syncs_default_feishu_when_index_is_empty(monkeypatch):
    """Default Feishu knowledge should be synced when configured and the index is empty."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        storage_mode = "memory"

        def document_count(self):
            return 0

        def hybrid_search(self, queries, k=4, status_filter=None):
            return []

    class FakeDefaultSyncer:
        def __init__(self, loader, retriever):
            self.synced_documents = []

        def sync_from_space(self, space_id):
            seen["space_id"] = space_id
            self.synced_documents = [
                Document(
                    page_content="默认知识库：营地应远离河谷、悬崖和孤树。",
                    metadata={"source": "feishu", "title": "默认营地指南"},
                )
            ]
            return [{"token": "doc-token", "title": "默认营地指南", "chunks": 1}]

    class FakeRewriter:
        def rewrite(self, question):
            return [question]

    class FakeReranker:
        @property
        def enabled(self):
            return False

    class FakeAugmenter:
        def augment(self, question, docs):
            seen["augmented_docs"] = docs
            return docs[0].page_content

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api.settings, "rag_docs_api_url", "")
    monkeypatch.setattr(rag_api.settings, "feishu_app_id", "app-id")
    monkeypatch.setattr(rag_api.settings, "feishu_app_secret", "app-secret")
    monkeypatch.setattr(rag_api.settings, "feishu_default_space_id", "space-1")
    monkeypatch.setattr(rag_api.settings, "feishu_default_folder_token", "")
    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "FeishuDefaultSyncer", FakeDefaultSyncer)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "营地选择注意什么"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["space_id"] == "space-1"
    assert seen["augmented_docs"][0].metadata["title"] == "默认营地指南"
    assert "知识库为空，正在同步默认飞书知识库" in body
    assert "默认知识库：营地应远离河谷" in body


def test_rag_irrelevant_retrieval_is_treated_as_no_match(monkeypatch):
    """If retrieval returns weak evidence, RAG should not answer from unrelated docs."""

    from api import rag as rag_api

    seen = {}

    class FakeRetriever:
        storage_mode = "memory"

        def similarity_search(self, query, k=2, status_filter=None):
            return [
                Document(
                    page_content="徒步时应携带足够的水和食物，注意天气变化。",
                    metadata={
                        "source": "upload",
                        "title": "徒步安全指南",
                        "file_name": "hiking_guide.md",
                    },
                )
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
            seen["docs"] = docs
            return "我没在知识库里找到和「量子物理是什么」直接相关的文档。"

    async def no_sleep(*_args, **_kwargs):
        return None

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", FakeRetriever)
    monkeypatch.setattr(rag_api, "QueryRewriter", FakeRewriter)
    monkeypatch.setattr(rag_api, "Reranker", FakeReranker)
    monkeypatch.setattr(rag_api, "ContextAugmenter", FakeAugmenter)
    monkeypatch.setattr(rag_api.asyncio, "sleep", no_sleep)

    client = TestClient(app)

    with client.stream("POST", "/api/v1/rag/query", json={"question": "量子物理是什么"}) as response:
        body = response.read().decode("utf-8")

    assert response.status_code == 200
    assert seen["docs"] == []
    assert '"searched_count": 0' in body
    assert "我没在知识库里找到" in body
    assert "徒步时应携带" not in body
