"""Tests for direct RAG answers that should not hit document retrieval."""

import os
import sys
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app


def test_simple_greeting_skips_retrieval(monkeypatch):
    """Simple greetings should answer directly without initializing retrieval."""

    from api import rag as rag_api

    class RetrieverShouldNotRun:
        def __init__(self):
            raise AssertionError("retriever should not run for simple greetings")

    monkeypatch.setattr(rag_api, "VectorStoreRetriever", RetrieverShouldNotRun)

    client = TestClient(app)
    with client.stream("POST", "/api/v1/rag/query", json={"question": "你好"}) as response:
        body = "\n".join(line for line in response.iter_lines() if line)

    assert response.status_code == 200
    assert "你好" in body
    assert "正在检索相关知识库" not in body
    assert '"type": "done"' in body
