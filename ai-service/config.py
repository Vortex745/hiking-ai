import os
import shutil
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))


class Settings:
    openai_base_url: str = ""
    openai_api_key: str = ""
    openai_model: str = "deepseek-v4-flash"
    embedding_base_url: str = ""
    embedding_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    rerank_base_url: str = ""
    rerank_api_key: str = ""
    rerank_model: str = "Qwen/Qwen3-Reranker-8B"
    rerank_top_k: int = 4
    rerank_timeout_seconds: float = 15.0
    rerank_enabled: bool = True
    database_url: str = "postgresql://ai_hiking:ai_hiking@localhost:5432/ai_hiking"
    redis_url: str = "redis://localhost:6379/0"
    feishu_default_space_id: str = ""
    feishu_default_folder_token: str = ""
    memory_store_path: str = "./memory_store"
    memory_top_k: int = 5
    memory_compressor_model: str = "deepseek-v4-flash"
    memory_extractor_model: str = "deepseek-v4-flash"
    memory_enabled: bool = True
    amap_api_key: str = ""

    def load(self) -> "Settings":
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "deepseek-v4-flash")
        self.embedding_base_url = os.getenv("EMBEDDING_BASE_URL", self.openai_base_url)
        self.embedding_api_key = os.getenv("EMBEDDING_API_KEY", self.openai_api_key)
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.embedding_dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1536"))
        self.rerank_base_url = os.getenv("RERANK_BASE_URL", self.embedding_base_url)
        self.rerank_api_key = os.getenv("RERANK_API_KEY", self.embedding_api_key)
        self.rerank_model = os.getenv("RERANK_MODEL", "Qwen/Qwen3-Reranker-8B")
        self.rerank_top_k = int(os.getenv("RERANK_TOP_K", "4"))
        self.rerank_timeout_seconds = float(os.getenv("RERANK_TIMEOUT_SECONDS", "15"))
        self.rerank_enabled = os.getenv("RERANK_ENABLED", "true").lower() == "true"
        self.database_url = os.getenv("DATABASE_URL", "postgresql://ai_hiking:ai_hiking@localhost:5432/ai_hiking")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.feishu_default_space_id = os.getenv("FEISHU_DEFAULT_SPACE_ID", "")
        self.feishu_default_folder_token = os.getenv("FEISHU_DEFAULT_FOLDER_TOKEN", "")
        self.memory_store_path = os.getenv("MEMORY_STORE_PATH", "./memory_store")
        self.memory_top_k = int(os.getenv("MEMORY_TOP_K", "5"))
        self.memory_compressor_model = os.getenv("MEMORY_COMPRESSOR_MODEL", "deepseek-v4-flash")
        self.memory_extractor_model = os.getenv("MEMORY_EXTRACTOR_MODEL", "deepseek-v4-flash")
        self.memory_enabled = os.getenv("MEMORY_ENABLED", "true").lower() == "true"
        self.amap_api_key = os.getenv("AMAP_API_KEY", "")

        return self

    @property
    def feishu_enabled(self) -> bool:
        return shutil.which("lark-cli") is not None


settings = Settings().load()
