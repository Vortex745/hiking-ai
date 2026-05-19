import asyncio
from types import SimpleNamespace

from langchain_core.documents import Document


def test_hiking_knowledge_search_returns_traceable_chunks(monkeypatch):
    from tools import hiking_knowledge

    class FakeRetriever:
        def hybrid_search(self, queries, k=4, status_filter=None):
            assert queries == ["失温怎么处理"]
            assert status_filter == "hiking"
            return [
                Document(
                    page_content="失温时应停止行进，补充保温层，尽快转移到避风处。",
                    metadata={
                        "source": "户外徒步知识文档.md",
                        "title": "失温处理",
                        "bm25_score": 3.2,
                    },
                )
            ]

    monkeypatch.setattr(hiking_knowledge, "VectorStoreRetriever", FakeRetriever)

    result = asyncio.run(hiking_knowledge.hiking_knowledge_search.ainvoke({"query": "失温怎么处理"}))

    assert result["query"] == "失温怎么处理"
    assert result["chunks"][0]["source"] == "户外徒步知识文档.md"
    assert result["chunks"][0]["title"] == "失温处理"
    assert "失温" in result["chunks"][0]["preview"]


def test_hiking_knowledge_search_reports_empty_evidence(monkeypatch):
    from tools import hiking_knowledge

    class FakeRetriever:
        def hybrid_search(self, queries, k=4, status_filter=None):
            return []

    monkeypatch.setattr(hiking_knowledge, "VectorStoreRetriever", FakeRetriever)

    result = asyncio.run(hiking_knowledge.hiking_knowledge_search.ainvoke({"query": "不存在的路线"}))

    assert result["chunks"] == []
    assert "资料不足" in result["message"]
