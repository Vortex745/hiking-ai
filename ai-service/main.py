import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ai-hiking AI Service...")
    logger.info(f"OpenAI Base URL: {settings.openai_base_url}")
    logger.info(f"OpenAI Model: {settings.openai_model}")
    yield
    logger.info("Shutting down ai-hiking AI Service...")


app = FastAPI(
    title="ai-hiking AI Service",
    description="Multi-modal AI Agent system with LangChain",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-service"}


# 注册路由——按依赖可用性逐个加载
# chat 路由: 需要 langgraph, langchain-core, openai
try:
    from api.chat import chat_router
    app.include_router(chat_router, prefix="/api/v1")
    logger.info("✓ Chat router loaded")
except ImportError as e:
    # 提供 fallback 端点
    from fastapi import APIRouter
    fallback = APIRouter()
    @fallback.get("/chat/health")
    async def chat_health():
        return {"status": "ok", "module": "chat", "fallback": "ai-service-health", "service": "fallback"}
    app.include_router(fallback, prefix="/api/v1")
    logger.warning(f"✗ Chat router unavailable: {e}")

# models 路由: 需要 openai, httpx
try:
    from api.models_router import models_router
    app.include_router(models_router, prefix="/api/v1")
    logger.info("✓ Models router loaded")
except ImportError as e:
    logger.warning(f"✗ Models router unavailable: {e}")

# rag 路由: 需要 langchain, faiss-cpu, etc
try:
    from api.rag import rag_router
    app.include_router(rag_router, prefix="/api/v1")
    logger.info("✓ RAG router loaded")
except ImportError as e:
    from fastapi import APIRouter
    fallback = APIRouter()
    @fallback.get("/rag/health")
    async def rag_health():
        return {"status": "ok", "module": "rag", "fallback": "ai-service-health", "service": "fallback"}
    app.include_router(fallback, prefix="/api/v1")
    logger.warning(f"✗ RAG router unavailable: {e}")

# tools 路由: 需要 httpx
try:
    from api.tools import tools_router
    app.include_router(tools_router, prefix="/api/v1")
    logger.info("✓ Tools router loaded")
except ImportError as e:
    logger.warning(f"✗ Tools router unavailable: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
