"""云知识库文档加载模块（基于远程 API）。

从远程 API 拉取文档内容，分块后返回 LangChain Document 列表。
"""

import logging

import httpx
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger("ai-service.rag.cloud_docs")


class CloudDocsLoader:
    """云知识库文档加载器：从远程 API 拉取文档 → 分块 → 返回 LangChain Document 列表。"""

    REQUEST_TIMEOUT = 30.0

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", ".", " ", ""],
        )

    def fetch_all_docs(self, api_url: str) -> list[dict]:
        try:
            resp = httpx.get(api_url, timeout=self.REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as e:
            raise RuntimeError(f"云知识库 API 请求失败: {e}")

        docs = data.get("docs", [])
        if not isinstance(docs, list):
            raise RuntimeError(f"云知识库 API 返回格式异常: 期望 docs 为列表，实际为 {type(docs).__name__}")

        return docs

    def load_and_split(self, api_url: str) -> list[Document]:
        raw_docs = self.fetch_all_docs(api_url)
        all_chunks: list[Document] = []

        for raw in raw_docs:
            name = raw.get("name", "unknown")
            content = raw.get("content", "")
            size = raw.get("size", 0)
            modified_at = raw.get("modifiedAt", "")

            if not content.strip():
                logger.warning("云知识库文档 %s 内容为空，跳过", name)
                continue

            chunks = self.splitter.create_documents([content])

            for chunk in chunks:
                chunk.metadata["source"] = "cloud_docs"
                chunk.metadata["title"] = name
                chunk.metadata["size"] = size
                chunk.metadata["modifiedAt"] = modified_at

            all_chunks.extend(chunks)
            logger.info("云知识库文档 %s → %d 个块", name, len(chunks))

        return all_chunks
