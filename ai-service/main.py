import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import chat_router
from api.models_router import models_router
from api.rag import rag_router
from api.tools import tools_router
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


app.include_router(chat_router, prefix="/api/v1")
app.include_router(models_router, prefix="/api/v1")
app.include_router(rag_router, prefix="/api/v1")
app.include_router(tools_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
