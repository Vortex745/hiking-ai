import asyncio
import json
import logging
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from api.models import (
    RAGQuery,
    RAGUploadResponse,
    RAGDocument,
    RuntimeModelSettings,
    FeishuSyncRequest,
    FeishuSyncResponse,
    FeishuDefaultSyncRequest,
    FeishuDefaultSyncResponse,
    FeishuDocRef,
)
from rag.loader import DocumentLoader
from rag.retriever import VectorStoreRetriever
from rag.feishu import FeishuDocLoader, FeishuDefaultSyncer, extract_doc_token, find_feishu_links
from config import settings
from rag.rewriter import QueryRewriter
from rag.augmenter import ContextAugmenter, has_relevant_evidence
from rag.reranker import Reranker
from rag.text_processing import clean_display_text

logger = logging.getLogger("ai-service.rag")
rag_router = APIRouter(prefix="/rag")

RAG_DOCS_DIR = Path("./rag_docs")
RAG_DOCS_DIR.mkdir(exist_ok=True)


DIRECT_ANSWER_PATTERNS = {
    "你好",
    "您好",
    "hi",
    "hello",
    "嗨",
    "你是谁",
    "你是谁？",
    "你是谁?",
    "谢谢",
    "谢谢你",
}


def direct_rag_answer(question: str) -> str | None:
    normalized = question.strip().lower().rstrip("。！？!?")
    if normalized in DIRECT_ANSWER_PATTERNS:
        if normalized in {"你是谁"}:
            return "我是 AI Hiking 的 RAG 助手，可以帮你检索知识库、总结文档，也可以回答一些简单问题。"
        if normalized in {"谢谢", "谢谢你"}:
            return "不客气。需要查知识库内容时，直接把问题发给我就行。"
        return "你好，我是 AI Hiking 的 RAG 助手。你可以上传文档后向我提问，也可以先问一些简单问题。"
    return None


def _runtime_llm_kwargs_from_settings(model_settings: RuntimeModelSettings | None) -> dict:
    if not model_settings or not model_settings.llm:
        return {}

    config = model_settings.llm
    return {
        "base_url": config.base_url,
        "api_key": config.api_key,
        "model": config.model,
    }


def _runtime_embedding_kwargs_from_settings(model_settings: RuntimeModelSettings | None) -> dict:
    if not model_settings or not model_settings.embedding:
        return {}

    config = model_settings.embedding
    return {
        "base_url": config.base_url,
        "api_key": config.api_key,
        "model": config.model,
        "dimensions": config.dimensions,
    }


def _runtime_rerank_kwargs_from_settings(model_settings: RuntimeModelSettings | None) -> dict:
    if not model_settings or not model_settings.rerank:
        return {}

    config = model_settings.rerank
    return {
        "base_url": config.base_url,
        "api_key": config.api_key,
        "model": config.model,
    }


def _parse_runtime_model_settings(raw: str | None) -> RuntimeModelSettings | None:
    if not raw:
        return None
    data = json.loads(raw)
    return RuntimeModelSettings(**data)


def _sse_event(event_type: str, content: str = "", metadata: dict | None = None) -> str:
    payload = {"type": event_type, "content": content}
    if metadata is not None:
        payload["metadata"] = metadata
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def _preview_text(text: str, limit: int = 260) -> str:
    normalized = clean_display_text(text)
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[:limit].rstrip()}..."


def _document_key(doc) -> str:
    metadata = doc.metadata or {}
    for key in ("feishu_wiki_node_token", "feishu_doc_token", "file_name", "source"):
        value = metadata.get(key)
        if value:
            return f"{key}:{value}"
    return f"content:{doc.page_content[:80]}"


def summarize_retrieved_documents(docs: list) -> dict:
    """Build a compact document-search summary for the frontend."""
    grouped: dict[str, dict] = {}

    for doc in docs:
        metadata = doc.metadata or {}
        key = _document_key(doc)
        current = grouped.setdefault(
            key,
            {
                "title": metadata.get("title") or metadata.get("file_name") or metadata.get("source") or "未命名文档",
                "source": metadata.get("source", "unknown"),
                "doc_type": metadata.get("feishu_doc_type") or metadata.get("doc_type") or "",
                "token": metadata.get("feishu_wiki_node_token") or metadata.get("feishu_doc_token") or "",
                "chunks": 0,
                "content": "",
            },
        )
        current["chunks"] += 1
        if not current["content"]:
            current["content"] = _preview_text(doc.page_content)

    documents = list(grouped.values())
    return {
        "searched_count": len(documents),
        "matched_chunks": len(docs),
        "documents": documents,
    }


def _dedupe_documents(docs: list) -> list:
    seen_keys: set[str] = set()
    deduped_docs = []
    for doc in docs:
        meta = doc.metadata or {}
        dedup_key = (
            meta.get("id")
            or meta.get("content_hash")
            or f"{meta.get('source', '')}:{doc.page_content[:100]}"
        )
        if dedup_key in seen_keys:
            continue
        seen_keys.add(dedup_key)
        deduped_docs.append(doc)
    return deduped_docs


@rag_router.get("/health")
async def rag_health():
    try:
        if not RAG_DOCS_DIR.exists():
            raise RuntimeError("RAG documents directory is missing")
        if not os.access(RAG_DOCS_DIR, os.W_OK):
            raise RuntimeError("RAG documents directory is not writable")

        retriever = VectorStoreRetriever()
        document_count = len([f for f in RAG_DOCS_DIR.iterdir() if f.is_file()])
        return {
            "status": "ok",
            "module": "rag",
            "service": "ai-service",
            "storage": retriever.storage_mode,
            "documents": document_count,
        }
    except Exception as e:
        logger.exception("RAG health check failed")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/upload")
async def rag_upload(
    file: UploadFile = File(...),
    status: str = Form(None),
    model_settings: str = Form(None),
):
    """Upload a document for RAG processing."""
    try:
        file_path = RAG_DOCS_DIR / file.filename
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        loader = DocumentLoader()
        docs = loader.load_and_split(str(file_path))

        runtime_settings = _parse_runtime_model_settings(model_settings)
        retriever = VectorStoreRetriever(**_runtime_embedding_kwargs_from_settings(runtime_settings))
        retriever.add_documents(docs, status)

        return RAGUploadResponse(
            filename=file.filename,
            chunks=len(docs),
            status=status or "none",
        )
    except Exception as e:
        logger.exception("Upload error")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/query")
async def rag_query(req: RAGQuery):
    """RAG query endpoint with SSE streaming."""

    async def event_stream():
        try:
            direct_answer = direct_rag_answer(req.question)
            if direct_answer is not None:
                yield _sse_event("text", direct_answer)
                yield _sse_event("done")
                return

            # 检测飞书 URL 并实时抓取文档
            feishu_docs: list = []
            if settings.feishu_enabled:
                yield _sse_event("process", "调用 lark-cli api 筛查飞书链接/知识库节点")
                await asyncio.sleep(0.2)
                try:
                    links = find_feishu_links(req.question)
                    if links:
                        yield _sse_event("process", f"识别到 {len(links)} 个飞书链接，开始读取可用内容")
                        await asyncio.sleep(0.2)
                        loader = FeishuDocLoader()
                        for link in links:
                            if link.kind == "wiki_space":
                                yield _sse_event(
                                    "process",
                                    "检测到飞书知识库空间链接，请先通过知识库同步入口同步空间内容",
                                    {"link_kind": link.kind, "token": link.token},
                                )
                                continue
                            feishu_docs.extend(loader.load_and_split(link.raw))
                        yield _sse_event("process", f"飞书链接读取完成，获得 {len(feishu_docs)} 个文档片段")
                    else:
                        yield _sse_event("process", "未发现需要实时读取的飞书链接，转入知识库检索")
                    await asyncio.sleep(0.2)
                except Exception as e:
                    logger.warning("飞书 URL 抓取失败，降级到普通搜索: %s", e)
                    yield _sse_event(
                        "process",
                        f"飞书链接读取失败：{e}。已转入普通知识库检索",
                        {"error": str(e)},
                    )
                    await asyncio.sleep(0.2)

            embedding_kwargs = _runtime_embedding_kwargs_from_settings(req.model_settings)
            try:
                retriever = VectorStoreRetriever(**embedding_kwargs)
            except Exception as e:
                logger.warning("自定义 Embedding 配置不可用，降级到默认配置: %s", e)
                retriever = VectorStoreRetriever()
                yield _sse_event(
                    "process",
                    f"自定义 Embedding 配置连接失败，已降级使用默认配置",
                    {"error": str(e)[:200]},
                )
            llm_kwargs = _runtime_llm_kwargs_from_settings(req.model_settings)
            rewriter = QueryRewriter(**llm_kwargs)
            try:
                augmenter = ContextAugmenter(**llm_kwargs)
            except Exception as e:
                logger.warning("自定义 LLM 配置不可用，降级到默认配置: %s", e)
                augmenter = ContextAugmenter()
            rerank_kwargs = _runtime_rerank_kwargs_from_settings(req.model_settings)
            try:
                reranker = Reranker(**rerank_kwargs)
            except Exception:
                reranker = Reranker()

            queries = rewriter.rewrite(req.question)
            yield _sse_event(
                "process",
                "调用查询改写模块生成检索查询：用户提问进入 query 改写",
                {"query_count": len(queries)},
            )
            await asyncio.sleep(0.2)

            yield _sse_event(
                "process",
                "调用 embedding 模型生成查询向量：问题向量化",
                {"query_count": len(queries)},
            )
            await asyncio.sleep(0.2)

            yield _sse_event(
                "process",
                "LangChain 混合检索组件开始召回：向量检索 + BM25",
                {"storage": getattr(retriever, "storage_mode", "unknown")},
            )
            await asyncio.sleep(0.2)

            all_docs = []
            retrieval_error = ""
            try:
                hybrid_search = getattr(retriever, "hybrid_search", None)
                if callable(hybrid_search):
                    all_docs = hybrid_search(queries, k=4, status_filter=req.status)
                else:
                    for q in queries:
                        all_docs.extend(retriever.similarity_search(q, k=2, status_filter=req.status))
                    all_docs = _dedupe_documents(all_docs)
            except Exception as e:
                retrieval_error = str(e)
                logger.warning("混合检索失败: %s", e)

            if retrieval_error and not all_docs and embedding_kwargs:
                logger.warning("自定义 Embedding 检索失败，降级到默认配置重试")
                yield _sse_event(
                    "process",
                    "自定义 Embedding 配置不可用，正在使用默认配置重试",
                    {"error": retrieval_error[:200]},
                )
                await asyncio.sleep(0.2)
                try:
                    retriever = VectorStoreRetriever()
                    hybrid_search = getattr(retriever, "hybrid_search", None)
                    if callable(hybrid_search):
                        all_docs = hybrid_search(queries, k=4, status_filter=req.status)
                    else:
                        for q in queries:
                            all_docs.extend(retriever.similarity_search(q, k=2, status_filter=req.status))
                        all_docs = _dedupe_documents(all_docs)
                    retrieval_error = ""
                except Exception as e:
                    retrieval_error = str(e)
                    logger.warning("默认 Embedding 混合检索也失败: %s", e)

            if not retrieval_error and not all_docs and embedding_kwargs:
                logger.warning("自定义 Embedding 未返回候选片段，使用默认配置重试")
                yield _sse_event(
                    "process",
                    "自定义 Embedding 未返回候选片段，正在使用默认配置重试",
                )
                await asyncio.sleep(0.2)
                try:
                    retriever = VectorStoreRetriever()
                    hybrid_search = getattr(retriever, "hybrid_search", None)
                    if callable(hybrid_search):
                        all_docs = hybrid_search(queries, k=4, status_filter=req.status)
                    else:
                        for q in queries:
                            all_docs.extend(retriever.similarity_search(q, k=2, status_filter=req.status))
                        all_docs = _dedupe_documents(all_docs)
                except Exception as e:
                    retrieval_error = str(e)
                    logger.warning("默认 Embedding 混合检索失败: %s", e)

            if retrieval_error and not all_docs:
                yield _sse_event(
                    "error",
                    f"混合检索失败：{retrieval_error[:200]}。请检查 Embedding 模型配置或网络连接。",
                    {"error": retrieval_error},
                )
                yield _sse_event("done")
                return

            yield _sse_event(
                "process",
                "使用向量在 pgvector/memory 中召回候选片段，并通过 BM25 + RRF 完成融合",
                {
                    "candidate_chunks": len(all_docs),
                    "storage": getattr(retriever, "storage_mode", "unknown"),
                },
            )
            await asyncio.sleep(0.2)

            all_docs = feishu_docs + all_docs
            if reranker.enabled and all_docs:
                yield _sse_event("process", "调用 Rerank 模型重排候选片段")
                await asyncio.sleep(0.2)
                all_docs = reranker.rerank(req.question, all_docs)
                yield _sse_event("process", f"Rerank 返回 {len(all_docs)} 个高相关片段")
                await asyncio.sleep(0.2)

            humanize_for_answer = getattr(rewriter, "humanize_for_answer", None)
            humanized_question = (
                humanize_for_answer(req.question)
                if callable(humanize_for_answer)
                else req.question
            )
            yield _sse_event(
                "process",
                "按 humanizer-zh 风格改写 query，用于最终回答",
                {"question": humanized_question},
            )
            await asyncio.sleep(0.2)

            if (
                all_docs
                and not feishu_docs
                and not has_relevant_evidence(req.question, all_docs)
                and not has_relevant_evidence(humanized_question, all_docs)
            ):
                yield _sse_event(
                    "process",
                    "检索片段与问题相关性不足，已按无匹配处理",
                    {"candidate_chunks": len(all_docs)},
                )
                all_docs = []

            document_summary = summarize_retrieved_documents(all_docs)
            yield _sse_event(
                "documents",
                f"已检索 {document_summary['searched_count']} 篇相关文档，共 {document_summary['matched_chunks']} 个片段",
                document_summary,
            )
            await asyncio.sleep(0.2)

            yield _sse_event("process", "构造上下文并调用 LLM 生成回答")
            try:
                # Try streaming first, fall back to sync
                has_streamed = False
                stream_fn = getattr(augmenter, "augment_stream", None)
                if callable(stream_fn):
                    async for chunk in stream_fn(humanized_question, all_docs):
                        yield _sse_event("text", chunk)
                        has_streamed = True
                if not has_streamed:
                    augmented = augmenter.augment(humanized_question, all_docs)
                    yield _sse_event("text", augmented)
            except Exception as e:
                logger.warning("LLM 生成回答失败: %s", e)
                context_preview = summarize_retrieved_documents(all_docs).get("documents", [])[:2]
                augmented = (
                    f"生成回答时出错：{e}\n\n"
                    f"但已检索到 {len(all_docs)} 个相关片段，以下是原始内容摘要：\n\n"
                    f"{chr(10).join(str(d) for d in context_preview)}\n\n"
                    f"原问题：{humanized_question}"
                )
                yield _sse_event("text", augmented)

            yield _sse_event("done")
        except Exception as e:
            logger.exception("RAG query error")
            yield _sse_event("error", str(e))

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@rag_router.get("/documents")
async def rag_documents():
    """List all uploaded documents."""
    docs = []
    for fpath in RAG_DOCS_DIR.iterdir():
        if fpath.is_file():
            docs.append(RAGDocument(
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, str(fpath))),
                filename=fpath.name,
                chunk_count=0,
            ))
    return {"documents": docs}


@rag_router.post("/feishu/sync", response_model=FeishuSyncResponse)
async def feishu_sync(req: FeishuSyncRequest):
    """同步飞书文档到 RAG 向量存储。

    从飞书拉取文档内容，按 Markdown 拆分后存入向量数据库，
    以便后续 RAG 检索。
    """
    if not settings.feishu_enabled:
        raise HTTPException(
            status_code=400,
            detail="飞书集成未启用，请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET",
        )

    try:
        doc_token = extract_doc_token(req.doc_token)
        doc_refs: list[FeishuDocRef] = []

        loader = FeishuDocLoader()
        docs = loader.load_and_split(
            doc_token=doc_token,
            title=req.title or doc_token,
            doc_type=req.doc_type,
        )

        retriever = VectorStoreRetriever()
        retriever.add_documents(docs, status="feishu")

        doc_refs.append(FeishuDocRef(
            token=doc_token,
            title=req.title or doc_token,
            chunks=len(docs),
        ))

        return FeishuSyncResponse(status="success", documents=doc_refs)

    except Exception as e:
        logger.exception("飞书文档同步失败")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/feishu/default-sync", response_model=FeishuDefaultSyncResponse)
async def feishu_default_sync(req: FeishuDefaultSyncRequest):
    """从飞书空间或文件夹批量同步文档到 RAG 向量存储。

    优先使用请求参数中的 space_id / folder_token，
    回退到环境变量 FEISHU_DEFAULT_SPACE_ID / FEISHU_DEFAULT_FOLDER_TOKEN。
    """
    if not settings.feishu_enabled:
        raise HTTPException(
            status_code=400,
            detail="飞书集成未启用：lark-cli 未安装或不在 PATH 中",
        )

    space_id = req.space_id or settings.feishu_default_space_id
    folder_token = req.folder_token or settings.feishu_default_folder_token

    if not space_id and not folder_token:
        raise HTTPException(
            status_code=400,
            detail="请设置 FEISHU_DEFAULT_SPACE_ID 或 FEISHU_DEFAULT_FOLDER_TOKEN 环境变量，"
                    "或在请求中提供 space_id / folder_token",
        )

    try:
        loader = FeishuDocLoader()
        retriever = VectorStoreRetriever()
        syncer = FeishuDefaultSyncer(loader, retriever)

        if folder_token:
            synced = syncer.sync_from_folder(folder_token)
        else:
            synced = syncer.sync_from_space(space_id)

        doc_refs = [
            FeishuDocRef(
                token=doc["token"],
                title=doc["title"],
                chunks=doc["chunks"],
            )
            for doc in synced
        ]

        return FeishuDefaultSyncResponse(
            status="success",
            synced_count=len(doc_refs),
            documents=doc_refs,
        )

    except Exception as e:
        logger.exception("飞书默认同步失败")
        raise HTTPException(status_code=500, detail=str(e))
