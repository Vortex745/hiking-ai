"""Tests for RAG ContextAugmenter — LangChain ChatPromptTemplate + streaming."""

import os
import sys
from pathlib import Path

from langchain_core.documents import Document

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_augmenter_no_docs_returns_fallback():
    """Without docs, augmenter should return a friendly no-docs message."""
    from rag.augmenter import ContextAugmenter

    augmenter = ContextAugmenter()
    result = augmenter.augment("徒步安全", [])
    assert "知识库" in result or "没" in result


def test_augmenter_no_llm_returns_context():
    """Without LLM config, augmenter should return a compact plain-text snippet."""
    from rag.augmenter import ContextAugmenter

    augmenter = ContextAugmenter(api_key="")  # no api_key → no LLM
    docs = [Document(page_content="徒步安全指南内容", metadata={"source": "test"})]
    result = augmenter.augment("徒步安全", docs)
    assert "徒步安全指南内容" in result
    assert "**" not in result
    assert "[1]" not in result


def test_augmenter_no_llm_does_not_dump_full_markdown_context():
    """No-LLM fallback should answer with compact points, not source/meta text."""
    from rag.augmenter import ContextAugmenter

    augmenter = ContextAugmenter(api_key="")
    long_content = "# 徒步的核心目的\n\n徒步的主要目的是**亲近自然**、挑战自我。" + "补充内容" * 300 + "[1]"
    docs = [
        Document(page_content=long_content, metadata={"source": "upload", "title": "户外徒步知识文档.md"}),
        Document(page_content="装备建议：穿专业登山鞋。", metadata={"source": "upload", "title": "徒步装备指南"}),
    ]

    result = augmenter.augment("徒步的核心目的", docs)

    assert "徒步的主要目的是亲近自然、挑战自我" in result
    assert "已检索" not in result
    assert "可先参考" not in result
    assert "文档" not in result
    assert "知识库" not in result
    assert result.startswith("1. ")
    assert "装备建议" not in result
    assert len(result) < 700
    assert "补充内容" * 50 not in result
    assert "#" not in result
    assert "**" not in result
    assert "[1]" not in result


def test_augmenter_no_llm_snippet_centers_question_terms():
    """Compact fallback should show the matched sentence, not only the document opening."""
    from rag.augmenter import ContextAugmenter

    augmenter = ContextAugmenter(api_key="")
    intro = "背景介绍" * 120
    content = f"{intro}。徒步的核心目的在于亲近自然、挑战自我、提升身心素质。后续说明" * 3
    docs = [Document(page_content=content, metadata={"source": "upload", "title": "户外徒步知识文档.md"})]

    result = augmenter.augment("徒步的核心目的", docs)

    assert "核心目的在于亲近自然" in result
    assert "背景介绍" * 30 not in result


def test_augmenter_no_llm_points_drop_truncated_neighbor_sentences():
    """Fallback points should not include clipped sentence fragments around the match."""
    from rag.augmenter import ContextAugmenter

    augmenter = ContextAugmenter(api_key="")
    docs = [
        Document(
            page_content=(
                "徒步（Hiking）是指在自然环境中进行的中长距离步行活动，区别于日常散步或短途健走。"
                "其核心目的在于亲近自然、挑战自我、提升身心素质。"
                "身体层面能增强心肺功能、提高耐力与协调性。"
                "心理层面能缓解精神压力。"
            ),
            metadata={"source": "test"},
        )
    ]

    result = augmenter.augment("徒步的核心目的", docs)

    assert "短途健走" not in result
    assert "1. 其核心目的在于亲近自然、挑战自我、提升身心素质。" in result
    assert "\n2. 身体层面能增强心肺功能、提高耐力与协调性。" in result


def test_augmenter_no_llm_points_drop_repeated_question_heading():
    """Fallback points should drop repeated heading text before the real fact."""
    from rag.augmenter import ContextAugmenter

    augmenter = ContextAugmenter(api_key="")
    docs = [
        Document(
            page_content="徒步的核心目的 徒步的价值体现在身体锻炼和心理成长。",
            metadata={"source": "test"},
        )
    ]

    result = augmenter.augment("徒步的核心目的", docs)

    assert "徒步的核心目的 徒步的价值" not in result
    assert "1. 徒步的价值体现在身体锻炼和心理成长。" in result


def test_augmenter_with_llm_invokes_model(monkeypatch):
    """With LLM configured, augmenter should invoke ChatModel with prompt template."""
    from rag.augmenter import ContextAugmenter

    invoked = {}

    class FakeAIMessage:
        content = "根据指南，徒步需注意安全。"

    class FakeChatModel:
        def invoke(self, prompt):
            invoked["prompt"] = prompt
            return FakeAIMessage()

        async def astream(self, prompt):
            for chunk in ["根据", "指南", "，徒步需注意安全。"]:
                class FakeChunk:
                    content = chunk
                yield FakeChunk()

    monkeypatch.setattr("rag.augmenter.ChatOpenAI", lambda **kw: FakeChatModel())

    augmenter = ContextAugmenter(api_key="test-key", base_url="http://fake", model="test")
    docs = [Document(page_content="安全内容", metadata={"source": "test"})]
    result = augmenter.augment("徒步安全", docs)

    assert "根据指南" in result
    assert invoked["prompt"] is not None


def test_augmenter_rejects_weakly_related_docs_even_with_llm(monkeypatch):
    """Weakly related retrieved docs should not be sent to the LLM."""
    from rag.augmenter import ContextAugmenter

    class FakeChatModel:
        def invoke(self, prompt):
            raise AssertionError("LLM should not be invoked for weak evidence")

        async def astream(self, prompt):
            raise AssertionError("LLM should not stream for weak evidence")
            yield

    monkeypatch.setattr("rag.augmenter.ChatOpenAI", lambda **kw: FakeChatModel())

    augmenter = ContextAugmenter(api_key="test-key", base_url="http://fake", model="test")
    docs = [
        Document(
            page_content="徒步时应携带足够的水和食物，注意天气变化。",
            metadata={"source": "test", "title": "徒步安全指南"},
        )
    ]
    result = augmenter.augment("量子物理是什么", docs)

    assert "没在知识库里找到" in result
    assert "量子物理" in result
    assert "徒步时应携带" not in result


def test_augmenter_prompt_requires_grounded_plain_text(monkeypatch):
    """The RAG prompt should force grounded plain text, not visible markdown."""
    from rag.augmenter import ContextAugmenter

    invoked = {}

    class FakeAIMessage:
        content = "根据文档，徒步要带**足够的水**。[1]"

    class FakeChatModel:
        def invoke(self, prompt):
            invoked["prompt"] = prompt
            return FakeAIMessage()

    monkeypatch.setattr("rag.augmenter.ChatOpenAI", lambda **kw: FakeChatModel())

    augmenter = ContextAugmenter(api_key="test-key", base_url="http://fake", model="test")
    docs = [Document(page_content="徒步要带水。", metadata={"source": "test"})]
    result = augmenter.augment("徒步要带什么", docs)

    prompt_text = "\n".join(getattr(message, "content", "") for message in invoked["prompt"])
    assert result == "徒步要带足够的水。"
    assert "每个关键事实" in prompt_text
    assert "不要写“根据文档”" in prompt_text
    assert "不要使用 Markdown 加粗" in prompt_text
    assert "文档外" in prompt_text


def test_augmenter_formats_long_answer_into_dense_points(monkeypatch):
    """Long generated answers should become readable numbered points."""
    from rag.augmenter import ContextAugmenter

    class FakeAIMessage:
        content = (
            "根据知识库内容，徒步的核心目的包括亲近自然、挑战自我、提升身心素质。"
            "身体层面能增强心肺功能、提高耐力与协调性。"
            "心理层面能缓解精神压力，规律参与人群焦虑指数平均下降42%。"
        )

    class FakeChatModel:
        def invoke(self, prompt):
            return FakeAIMessage()

    monkeypatch.setattr("rag.augmenter.ChatOpenAI", lambda **kw: FakeChatModel())

    augmenter = ContextAugmenter(api_key="test-key", base_url="http://fake", model="test")
    docs = [
        Document(
            page_content="徒步的核心目的包括亲近自然、挑战自我、提升身心素质。规律参与可缓解精神压力。",
            metadata={"source": "test"},
        )
    ]

    result = augmenter.augment("徒步的核心目的", docs)

    assert "文档" not in result
    assert "知识库" not in result
    assert "1. 徒步的核心目的包括亲近自然、挑战自我、提升身心素质。" in result
    assert "\n2. 身体层面能增强心肺功能、提高耐力与协调性。" in result
    assert "\n3. 心理层面能缓解精神压力" in result


def test_augmenter_stream_outputs_plain_text(monkeypatch):
    """Streaming answers should also hide markdown emphasis and numeric citations."""
    import asyncio
    from rag.augmenter import ContextAugmenter

    class FakeChatModel:
        async def astream(self, prompt):
            for chunk in ["徒步的主要目的是", "**亲近自然**", "。[1]"]:
                class Ch:
                    content = chunk
                yield Ch()

    monkeypatch.setattr("rag.augmenter.ChatOpenAI", lambda **kw: FakeChatModel())

    augmenter = ContextAugmenter(api_key="test-key", base_url="http://fake", model="test")
    docs = [Document(page_content="徒步的主要目的是亲近自然。", metadata={"source": "test"})]

    async def collect():
        chunks = []
        async for chunk in augmenter.augment_stream("徒步的主要目的", docs):
            chunks.append(chunk)
        return "".join(chunks)

    result = asyncio.run(collect())
    assert result == "徒步的主要目的是亲近自然。"


def test_augmenter_stream_returns_async_iterator(monkeypatch):
    """augment_stream should return an async iterator of string chunks."""
    import asyncio
    from rag.augmenter import ContextAugmenter

    class FakeChunk:
        content = "chunk"

    class FakeChatModel:
        async def astream(self, prompt):
            for c in ["你", "好"]:
                class Ch:
                    content = c
                yield Ch()

    monkeypatch.setattr("rag.augmenter.ChatOpenAI", lambda **kw: FakeChatModel())

    augmenter = ContextAugmenter(api_key="test-key", base_url="http://fake", model="test")
    docs = [Document(page_content="徒步内容", metadata={"source": "test"})]

    async def collect():
        chunks = []
        async for chunk in augmenter.augment_stream("徒步", docs):
            chunks.append(chunk)
        return chunks

    chunks = asyncio.run(collect())
    assert "".join(chunks) == "你好"


def test_inject_knowledge_returns_prompt():
    """inject_knowledge should build a prompt string from knowledge items."""
    from rag.augmenter import ContextAugmenter

    augmenter = ContextAugmenter()
    items = [
        {"content": "徒步带水", "type": "常识", "confidence": 0.9},
    ]
    result = augmenter.inject_knowledge("徒步准备", items)
    assert "徒步带水" in result
    assert "90%" in result
