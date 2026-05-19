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

    # 验证检索被调用
    assert seen["search_query"] == "徒步需要准备什么"
    assert seen["rewritten"] == "徒步需要准备什么"

    # 验证文档被传递给 augmenter
    assert len(seen["augmented_docs"]) == 2
    assert "徒步时应携带足够的水和食物" in seen["augmented_docs"][0]
    assert "防滑登山鞋" in seen["augmented_docs"][1]
    assert seen["augmented_question"] == "徒步需要准备什么"

    # 验证 SSE 输出包含文档检索事件
    assert '"type": "documents"' in body
    assert '"searched_count": 2' in body
    assert '"matched_chunks": 2' in body
    assert "徒步安全指南" in body
    assert "装备清单" in body

    # 验证最终答案输出
    assert '"type": "text"' in body
    assert "根据徒步安全指南" in body
    assert "防滑登山鞋和急救包" in body

    # 验证流结束
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


def test_feishu_file_type_download(monkeypatch, tmp_path):
    """FeishuDocLoader should download file-type documents via drive API."""

    from rag.feishu import FeishuDocLoader, _DOWNLOADABLE_TYPES

    assert "file" in _DOWNLOADABLE_TYPES

    loader = FeishuDocLoader()

    downloaded_file = tmp_path / "test_doc.md"
    downloaded_file.write_text("# 测试文档\n\n这是飞书文件类型文档的内容。", encoding="utf-8")

    def fake_call_lark_api(method, path, params=None, data=None):
        if "/download" in path:
            return {"saved_path": str(downloaded_file), "content_type": "text/markdown; charset=utf-8", "size_bytes": 100}
        raise RuntimeError(f"unexpected API call: {method} {path}")

    import rag.feishu as feishu_mod
    monkeypatch.setattr(feishu_mod, "call_lark_api", fake_call_lark_api)

    result = loader.fetch_content("fake_file_token", doc_type="file")
    assert "测试文档" in result["markdown"]
    assert "飞书文件类型文档" in result["markdown"]
    assert result["doc_id"] == "fake_file_token"


def test_feishu_wiki_permission_fallback_to_download(monkeypatch, tmp_path):
    """When Wiki API permission denied, _resolve_document_ref should fallback to file download."""

    from rag.feishu import FeishuDocLoader

    loader = FeishuDocLoader()

    downloaded_file = tmp_path / "wiki_doc.md"
    downloaded_file.write_text("# Wiki文档\n\nWiki节点内容。", encoding="utf-8")

    def fake_call_lark_api(method, path, params=None, data=None):
        if "get_node" in path:
            raise RuntimeError("lark-cli API 错误: Permission denied [99991679]")
        if "/download" in path:
            return {"saved_path": str(downloaded_file), "content_type": "text/markdown; charset=utf-8", "size_bytes": 100}
        raise RuntimeError(f"unexpected API call: {method} {path}")

    import rag.feishu as feishu_mod
    monkeypatch.setattr(feishu_mod, "call_lark_api", fake_call_lark_api)

    docs = loader.load_and_split(
        doc_token="https://example.feishu.cn/wiki/WikiNodeToken1234567890ab",
        title="Wiki文档",
        doc_type="wiki",
    )
    assert len(docs) > 0
    assert "Wiki节点内容" in docs[0].page_content
    assert docs[0].metadata["source"] == "feishu"
