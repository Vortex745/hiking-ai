"""Tests for the RAG document upload pipeline."""

import os
import sys
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_document_loader_cleans_chunks_and_tags_metadata(tmp_path):
    """Uploaded docs should be normalized, denoised, chunked, and tagged."""

    from rag.loader import DocumentLoader

    source = tmp_path / "gear.md"
    source.write_text(
        "# 徒步装备!!!\n\n"
        "头灯、雨衣、GPS@@@ 都要提前检查。\n\n"
        "无效符号 ### $$$ 应该被清理。",
        encoding="utf-8",
    )

    loader = DocumentLoader(chunk_size=24, chunk_overlap=4)
    docs = loader.load_and_split(str(source))

    assert len(docs) >= 2
    joined = "\n".join(doc.page_content for doc in docs)
    assert "!" not in joined
    assert "@" not in joined
    assert "#" not in joined
    assert "$" not in joined
    assert "徒步装备" in joined

    for index, doc in enumerate(docs):
        assert doc.metadata["source"] == source.name
        assert doc.metadata["file_name"] == source.name
        assert doc.metadata["title"] == "徒步装备"
        assert doc.metadata["chunk_index"] == index
        assert doc.metadata["chunk_count"] == len(docs)
        assert doc.metadata["chunk_strategy"] == "hybrid_recursive"
        assert doc.metadata["content_hash"]
