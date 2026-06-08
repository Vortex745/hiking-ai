import asyncio
import json
import logging
import os
import re
import uuid

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from api.models import (
    RAGQuery,
    RAGUploadResponse,
    RAGDocument,
    RuntimeModelSettings,
)
from config import settings
from memory.factory import chat_memory_status, get_chat_memory
from runtime_paths import runtime_dir

logger = logging.getLogger("ai-service.rag")
rag_router = APIRouter(prefix="/rag")

RAG_DOCS_DIR = runtime_dir("RAG_DOCS_DIR", "rag_docs")

DocumentLoader = None
VectorStoreRetriever = None
CloudDocsLoader = None
QueryRewriter = None
ContextAugmenter = None
Reranker = None
FeishuDefaultSyncer = None
FeishuDocLoader = None
find_feishu_links = None
has_relevant_evidence = None
clean_display_text = None


def _get_document_loader_class():
    global DocumentLoader
    if DocumentLoader is None:
        from rag.loader import DocumentLoader as loaded

        DocumentLoader = loaded
    return DocumentLoader


def _get_vector_store_retriever_class():
    global VectorStoreRetriever
    if VectorStoreRetriever is None:
        from rag.retriever import VectorStoreRetriever as loaded

        VectorStoreRetriever = loaded
    return VectorStoreRetriever


def _get_cloud_docs_loader_class():
    global CloudDocsLoader
    if CloudDocsLoader is None:
        from rag.cloud_docs import CloudDocsLoader as loaded

        CloudDocsLoader = loaded
    return CloudDocsLoader


def _get_query_rewriter_class():
    global QueryRewriter
    if QueryRewriter is None:
        from rag.rewriter import QueryRewriter as loaded

        QueryRewriter = loaded
    return QueryRewriter


def _get_context_augmenter_class():
    global ContextAugmenter
    if ContextAugmenter is None:
        from rag.augmenter import ContextAugmenter as loaded

        ContextAugmenter = loaded
    return ContextAugmenter


def _get_reranker_class():
    global Reranker
    if Reranker is None:
        from rag.reranker import Reranker as loaded

        Reranker = loaded
    return Reranker


def _get_feishu_classes():
    global FeishuDefaultSyncer, FeishuDocLoader
    if FeishuDefaultSyncer is None:
        from rag.feishu import FeishuDefaultSyncer as loaded_syncer

        FeishuDefaultSyncer = loaded_syncer
    if FeishuDocLoader is None:
        from rag.feishu import FeishuDocLoader as loaded_loader

        FeishuDocLoader = loaded_loader
    return FeishuDefaultSyncer, FeishuDocLoader


def _find_feishu_links(text: str):
    global find_feishu_links
    if find_feishu_links is None:
        from rag.feishu import find_feishu_links as loaded

        find_feishu_links = loaded
    return find_feishu_links(text)


def _has_relevant_evidence(question: str, docs: list) -> bool:
    global has_relevant_evidence
    if has_relevant_evidence is None:
        from rag.augmenter import has_relevant_evidence as loaded

        has_relevant_evidence = loaded
    return has_relevant_evidence(question, docs)


def _clean_display_text(text: str) -> str:
    global clean_display_text
    if clean_display_text is None:
        from rag.text_processing import clean_display_text as loaded

        clean_display_text = loaded
    return clean_display_text(text)


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

FOLLOW_UP_MARKERS = {"这些", "这个", "这类", "它", "他们", "它们", "那", "上述", "上面", "刚才", "呢"}

HIKING_INTENT_TERMS = {
    "徒步",
    "登山",
    "爬山",
    "户外",
    "露营",
    "营地",
    "路线",
    "轨迹",
    "行程",
    "装备",
    "背包",
    "登山鞋",
    "冲锋衣",
    "登山杖",
    "头灯",
    "补给",
    "饮水",
    "急救",
    "导航",
    "海拔",
    "高反",
    "失温",
    "下撤",
    "穿越",
    "重装",
    "轻装",
    "雨天",
    "山洪",
}

AMBIGUOUS_ACTIVITY_TERMS = {"活动", "带我", "参加", "报名"}

RAG_UNCLEAR_MSG = "我没理解你的问题。可以换成一个具体的徒步问题，比如路线、装备、天气风险、营地选择或急救处理。"
RAG_AMBIGUOUS_ACTIVITY_MSG = "你是想问徒步活动吗？请补充目的地、天数、难度或你想了解的具体问题，我再帮你查知识库。"
RAG_OUT_OF_DOMAIN_MSG = "这个问题看起来不属于徒步知识库范围。你可以问徒步路线、装备、天气风险、营地选择、补给或急救相关问题。"


def direct_rag_answer(question: str) -> str | None:
    normalized = question.strip().lower().rstrip("。！？!?")
    if normalized in DIRECT_ANSWER_PATTERNS:
        if normalized in {"你是谁"}:
            return "我是 AI Hiking 的 RAG 助手，可以帮你检索知识库、总结文档，也可以回答一些简单问题。"
        if normalized in {"谢谢", "谢谢你"}:
            return "不客气。需要查知识库内容时，直接把问题发给我就行。"
        return "你好，我是 AI Hiking 的 RAG 助手。你可以上传文档后向我提问，也可以先问一些简单问题。"
    return None


def _compact_question_text(question: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", question).strip().lower()


def _has_previous_user_message(history: list[dict]) -> bool:
    return any(item.get("role") == "user" and str(item.get("content") or "").strip() for item in history)


def _is_follow_up_question(question: str, history: list[dict]) -> bool:
    return _has_previous_user_message(history) and any(marker in question for marker in FOLLOW_UP_MARKERS)


def _has_hiking_intent(question: str) -> bool:
    lowered = question.lower()
    return any(term.lower() in lowered for term in HIKING_INTENT_TERMS)


def _rag_guard_answer(question: str, history: list[dict]) -> str | None:
    """Return a direct guard answer when a query should not enter retrieval."""
    if _find_feishu_links(question):
        return None

    compact = _compact_question_text(question)
    if not compact:
        return RAG_UNCLEAR_MSG

    if _is_follow_up_question(question, history):
        return None

    if _has_hiking_intent(question):
        return None

    if len(compact) < 4:
        return RAG_UNCLEAR_MSG

    if any(term in compact for term in AMBIGUOUS_ACTIVITY_TERMS):
        return RAG_AMBIGUOUS_ACTIVITY_MSG

    return RAG_OUT_OF_DOMAIN_MSG


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


def _recent_rag_history(memory, limit: int = 6) -> list[dict]:
    if memory is None:
        return []
    try:
        messages = memory.get_messages()
    except Exception as e:
        logger.warning("读取 RAG 历史失败，跳过上下文改写: %s", e)
        return []

    if not isinstance(messages, list):
        return []

    normalized: list[dict] = []
    for item in messages[-limit:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if isinstance(role, str) and isinstance(content, str) and content.strip():
            normalized.append({"role": role, "content": content})
    return normalized


def _preview_text(text: str, limit: int = 260) -> str:
    normalized = _clean_display_text(text)
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[:limit].rstrip()}..."


def _document_key(doc) -> str:
    metadata = doc.metadata or {}
    for key in ("title", "file_name", "source"):
        value = metadata.get(key)
        if value:
            return f"{key}:{value}"
    return f"content:{doc.page_content[:80]}"


def _document_filename(doc) -> str:
    metadata = doc.metadata or {}
    return (
        metadata.get("title")
        or metadata.get("file_name")
        or metadata.get("source")
        or metadata.get("id")
        or "indexed-document"
    )


def _indexed_document_refs(retriever: VectorStoreRetriever) -> list[RAGDocument]:
    grouped: dict[str, RAGDocument] = {}
    for doc in retriever.indexed_documents():
        key = _document_key(doc)
        metadata = doc.metadata or {}
        current = grouped.get(key)
        if current is None:
            grouped[key] = RAGDocument(
                id=str(uuid.uuid5(uuid.NAMESPACE_URL, key)),
                filename=str(_document_filename(doc)),
                status=metadata.get("status"),
                chunk_count=1,
            )
        else:
            current.chunk_count += 1
    return list(grouped.values())


def summarize_retrieved_documents(docs: list) -> dict:
    grouped: dict[str, dict] = {}

    for doc in docs:
        metadata = doc.metadata or {}
        key = _document_key(doc)
        current = grouped.setdefault(
            key,
            {
                "title": metadata.get("title") or metadata.get("file_name") or metadata.get("source") or "未命名文档",
                "source": metadata.get("source", "unknown"),
                "doc_type": metadata.get("doc_type") or "",
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


def _persist_rag_message(memory, role: str, content: str) -> None:
    if memory is None or not content:
        return
    try:
        memory.add_message(role, content)
    except Exception as exc:
        logger.warning("RAG chat persistence failed for role=%s: %s", role, exc)


def _summarize_feishu_sync(summaries: list[dict]) -> dict:
    synced_count = sum(1 for item in summaries if not item.get("error") and item.get("chunks", 0) > 0)
    error_count = sum(1 for item in summaries if item.get("error"))
    chunk_count = sum(int(item.get("chunks") or 0) for item in summaries)
    return {
        "synced_count": synced_count,
        "error_count": error_count,
        "chunks": chunk_count,
        "documents": summaries,
    }


def _sync_feishu_links(question: str, retriever: VectorStoreRetriever) -> tuple[list, list[dict]]:
    links = _find_feishu_links(question)
    if not links:
        return [], []

    syncer_cls, loader_cls = _get_feishu_classes()
    loader = loader_cls()
    syncer = syncer_cls(loader, retriever)
    summaries: list[dict] = []
    synced_docs = []

    for link in links:
        try:
            if link.kind == "wiki_space":
                summaries.extend(syncer.sync_from_space(link.token))
                continue

            docs = loader.load_and_split(link.raw, doc_type=link.doc_type)
            retriever.add_documents(docs, status="feishu")
            syncer.synced_documents.extend(docs)
            synced_docs.extend(docs)
            title = docs[0].metadata.get("title", link.token) if docs else link.token
            summaries.append({"token": link.token, "title": title, "chunks": len(docs)})
        except Exception as exc:
            logger.warning("Feishu link sync failed: %s", exc)
            summaries.append({"token": link.token, "title": link.token, "chunks": 0, "error": str(exc)})

    return syncer.synced_documents or synced_docs, summaries


def _sync_default_feishu_knowledge(retriever: VectorStoreRetriever) -> tuple[list, list[dict]]:
    syncer_cls, loader_cls = _get_feishu_classes()
    loader = loader_cls()
    syncer = syncer_cls(loader, retriever)
    summaries: list[dict] = []

    if settings.feishu_default_space_id:
        summaries.extend(syncer.sync_from_space(settings.feishu_default_space_id))
    if settings.feishu_default_folder_token:
        summaries.extend(syncer.sync_from_folder(settings.feishu_default_folder_token))

    return syncer.synced_documents, summaries


@rag_router.get("/health")
async def rag_health():
    try:
        if not RAG_DOCS_DIR.exists():
            raise RuntimeError("RAG documents directory is missing")
        if not os.access(RAG_DOCS_DIR, os.W_OK):
            raise RuntimeError("RAG documents directory is not writable")

        retriever_cls = _get_vector_store_retriever_class()
        retriever = retriever_cls()
        document_count = retriever.document_count()
        return {
            "status": "ok",
            "module": "rag",
            "service": "ai-service",
            "storage": retriever.storage_mode,
            "documents": document_count,
            "rag_docs_api_configured": bool(settings.rag_docs_api_url),
            "feishu_enabled": settings.feishu_enabled,
            "feishu_default_configured": settings.feishu_default_configured,
            "memory": chat_memory_status(),
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

        loader_cls = _get_document_loader_class()
        loader = loader_cls()
        docs = loader.load_and_split(str(file_path))

        runtime_settings = _parse_runtime_model_settings(model_settings)
        retriever_cls = _get_vector_store_retriever_class()
        retriever = retriever_cls(**_runtime_embedding_kwargs_from_settings(runtime_settings))
        indexing_result = retriever.add_documents(docs, status)
        if (
            indexing_result is not None
            and getattr(indexing_result, "requested_count", len(docs)) > 0
            and (
                getattr(indexing_result, "indexed_count", len(docs)) < len(docs)
                or getattr(indexing_result, "fallback_used", False)
                or (
                    settings.postgres_configured
                    and not getattr(indexing_result, "durable", False)
                )
            )
        ):
            detail = "文档已接收，但未写入持久向量索引，暂时不能用于知识库检索。"
            error = getattr(indexing_result, "error", None)
            if error:
                detail = f"{detail} 原因：{error}"
            raise HTTPException(status_code=503, detail=detail)

        return RAGUploadResponse(
            filename=file.filename,
            chunks=len(docs),
            status=status or "none",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upload error")
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.post("/query")
async def rag_query(req: RAGQuery):
    """RAG query endpoint with SSE streaming."""

    async def event_stream():
        memory = get_chat_memory(req.chat_id) if req.chat_id else None
        assistant_parts: list[str] = []
        try:
            history_messages = _recent_rag_history(memory)
            _persist_rag_message(memory, "user", req.question)
            direct_answer = direct_rag_answer(req.question)
            if direct_answer is not None:
                assistant_parts.append(direct_answer)
                yield _sse_event("text", direct_answer)
                _persist_rag_message(memory, "assistant", "".join(assistant_parts).strip())
                yield _sse_event("done")
                return

            guard_answer = _rag_guard_answer(req.question, history_messages)
            if guard_answer is not None:
                yield _sse_event(
                    "process",
                    "问题不清晰或超出徒步知识库范围，跳过知识库检索",
                )
                assistant_parts.append(guard_answer)
                yield _sse_event("text", guard_answer)
                _persist_rag_message(memory, "assistant", "".join(assistant_parts).strip())
                yield _sse_event("done")
                return

            embedding_kwargs = _runtime_embedding_kwargs_from_settings(req.model_settings)
            try:
                retriever_cls = _get_vector_store_retriever_class()
                retriever = retriever_cls(**embedding_kwargs)
            except Exception as e:
                logger.warning("自定义 Embedding 配置不可用，降级到默认配置: %s", e)
                retriever_cls = _get_vector_store_retriever_class()
                retriever = retriever_cls()
                yield _sse_event(
                    "process",
                    f"自定义 Embedding 配置连接失败，已降级使用默认配置",
                    {"error": str(e)[:200]},
                )

            cloud_docs: list = []
            if settings.rag_docs_api_url:
                yield _sse_event("process", "从云知识库 API 同步文档")
                await asyncio.sleep(0.2)
                try:
                    cloud_loader_cls = _get_cloud_docs_loader_class()
                    cloud_loader = cloud_loader_cls()
                    loaded = cloud_loader.load_and_split(settings.rag_docs_api_url)
                    if loaded:
                        retriever.add_documents(loaded, status="cloud_docs")
                        cloud_docs.extend(loaded)
                    yield _sse_event(
                        "process",
                        (
                            f"已同步云知识库文档，获得 {len(loaded)} 个文档片段"
                            if loaded
                            else "云知识库同步未获得文档片段，请检查 API 地址及返回数据"
                        ),
                        {
                            "source": "cloud_docs_api",
                            "api_url": settings.rag_docs_api_url,
                            "chunks": len(loaded),
                        },
                    )
                except Exception as e:
                    logger.warning("云知识库 API 同步失败: %s", e)
                    yield _sse_event(
                        "process",
                        f"云知识库同步失败：{e}。已转入普通知识库检索",
                        {"error": str(e)},
                    )
                await asyncio.sleep(0.2)

            feishu_docs: list = []
            feishu_links = _find_feishu_links(req.question)
            if feishu_links and not settings.feishu_enabled:
                yield _sse_event(
                    "process",
                    "检测到飞书链接，但飞书应用凭证未配置，已转入普通知识库检索",
                    {"link_count": len(feishu_links)},
                )
                await asyncio.sleep(0.2)
                answer = "我检测到了飞书链接，但当前服务没有配置飞书应用凭证，暂时不能读取该文档。请先配置飞书凭证，或把文档导出后上传到知识库。"
                assistant_parts.append(answer)
                yield _sse_event("text", answer)
                _persist_rag_message(memory, "assistant", "".join(assistant_parts).strip())
                yield _sse_event("done")
                return
            elif feishu_links:
                yield _sse_event(
                    "process",
                    "检测到飞书链接，正在同步飞书文档",
                    {"link_count": len(feishu_links)},
                )
                await asyncio.sleep(0.2)
                feishu_docs, summaries = _sync_feishu_links(req.question, retriever)
                sync_summary = _summarize_feishu_sync(summaries)
                yield _sse_event(
                    "process",
                    (
                        f"已同步飞书文档，获得 {sync_summary['chunks']} 个文档片段"
                        if sync_summary["chunks"]
                        else "飞书文档同步未获得文档片段，请检查链接权限"
                    ),
                    sync_summary,
                )
                await asyncio.sleep(0.2)
                if not feishu_docs:
                    answer = "我检测到了飞书链接，但没有同步到可检索的文档内容。请确认飞书应用对该文档有访问权限，或先把文档导出/上传后再问。"
                    assistant_parts.append(answer)
                    yield _sse_event("text", answer)
                    _persist_rag_message(memory, "assistant", "".join(assistant_parts).strip())
                    yield _sse_event("done")
                    return
            elif (
                not cloud_docs
                and settings.feishu_enabled
                and settings.feishu_default_configured
                and retriever.document_count() == 0
            ):
                yield _sse_event("process", "知识库为空，正在同步默认飞书知识库")
                await asyncio.sleep(0.2)
                feishu_docs, summaries = _sync_default_feishu_knowledge(retriever)
                sync_summary = _summarize_feishu_sync(summaries)
                yield _sse_event(
                    "process",
                    (
                        f"已同步默认飞书知识库，获得 {sync_summary['chunks']} 个文档片段"
                        if sync_summary["chunks"]
                        else "默认飞书知识库同步未获得文档片段，请检查空间/文件夹权限"
                    ),
                    sync_summary,
                )
                await asyncio.sleep(0.2)

            llm_kwargs = _runtime_llm_kwargs_from_settings(req.model_settings)
            rewriter_cls = _get_query_rewriter_class()
            rewriter = rewriter_cls(**llm_kwargs)
            try:
                augmenter_cls = _get_context_augmenter_class()
                augmenter = augmenter_cls(**llm_kwargs)
            except Exception as e:
                logger.warning("自定义 LLM 配置不可用，降级到默认配置: %s", e)
                augmenter_cls = _get_context_augmenter_class()
                augmenter = augmenter_cls()
            rerank_kwargs = _runtime_rerank_kwargs_from_settings(req.model_settings)
            try:
                reranker_cls = _get_reranker_class()
                reranker = reranker_cls(**rerank_kwargs)
            except Exception:
                reranker_cls = _get_reranker_class()
                reranker = reranker_cls()

            contextualize = getattr(rewriter, "contextualize", None)
            contextual_question = (
                contextualize(req.question, history_messages)
                if callable(contextualize)
                else req.question
            )
            if contextual_question != req.question:
                yield _sse_event(
                    "process",
                    "结合历史上下文改写当前问题，用于检索",
                    {"question": contextual_question},
                )
                await asyncio.sleep(0.2)

            queries = rewriter.rewrite(contextual_question)
            yield _sse_event(
                "process",
                "调用查询改写模块生成检索查询：用户提问进入 query 改写",
                {"query_count": len(queries), "question": contextual_question},
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
                    retriever_cls = _get_vector_store_retriever_class()
                    retriever = retriever_cls()
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
                    retriever_cls = _get_vector_store_retriever_class()
                    retriever = retriever_cls()
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
                all_docs = reranker.rerank(contextual_question, all_docs)
                yield _sse_event("process", f"Rerank 返回 {len(all_docs)} 个高相关片段")
                await asyncio.sleep(0.2)

            humanize_for_answer = getattr(rewriter, "humanize_for_answer", None)
            humanized_question = (
                humanize_for_answer(contextual_question)
                if callable(humanize_for_answer)
                else contextual_question
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
                and not _has_relevant_evidence(contextual_question, all_docs)
                and not _has_relevant_evidence(humanized_question, all_docs)
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
                has_streamed = False
                stream_fn = getattr(augmenter, "augment_stream", None)
                if callable(stream_fn):
                    async for chunk in stream_fn(humanized_question, all_docs):
                        assistant_parts.append(chunk)
                        yield _sse_event("text", chunk)
                        has_streamed = True
                if not has_streamed:
                    augmented = augmenter.augment(humanized_question, all_docs)
                    assistant_parts.append(augmented)
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
                assistant_parts.append(augmented)
                yield _sse_event("text", augmented)

            _persist_rag_message(memory, "assistant", "".join(assistant_parts).strip())
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
    retriever_cls = _get_vector_store_retriever_class()
    retriever = retriever_cls()
    docs = _indexed_document_refs(retriever)
    if not docs:
        for fpath in RAG_DOCS_DIR.iterdir():
            if fpath.is_file():
                docs.append(RAGDocument(
                    id=str(uuid.uuid5(uuid.NAMESPACE_URL, str(fpath))),
                    filename=fpath.name,
                    chunk_count=0,
                ))
    return {"documents": docs}


@rag_router.get("/history/{chat_id}")
async def rag_history(chat_id: str):
    """Get persisted RAG chat history for a given chat_id."""
    try:
        memory = get_chat_memory(chat_id)
        return {"chat_id": chat_id, "messages": memory.get_messages()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@rag_router.delete("/history/{chat_id}")
async def rag_clear_history(chat_id: str):
    """Clear persisted RAG chat history for a given chat_id."""
    try:
        memory = get_chat_memory(chat_id)
        memory.clear()
        return {"chat_id": chat_id, "status": "cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
