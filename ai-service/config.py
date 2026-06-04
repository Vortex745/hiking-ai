import os
import json
from pathlib import Path

from dotenv import load_dotenv


if not os.getenv("VERCEL"):
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
    database_url_source: str = ""
    database_connect_timeout_seconds: int = 2
    redis_url: str = "redis://localhost:6379/0"
    redis_url_source: str = ""
    redis_rest_url: str = ""
    redis_rest_url_source: str = ""
    redis_rest_token: str = ""
    redis_rest_token_source: str = ""
    rag_docs_api_url: str = ""
    feishu_app_id: str = ""
    feishu_app_secret: str = ""
    feishu_default_space_id: str = ""
    feishu_default_folder_token: str = ""
    memory_store_path: str = "./memory_store"
    memory_top_k: int = 5
    memory_compressor_model: str = "deepseek-v4-flash"
    memory_extractor_model: str = "deepseek-v4-flash"
    memory_enabled: bool = True
    amap_api_key: str = ""
    mcp_servers: dict = {}
    mcp_capability_map: dict = {}
    disabled_lanes: str = ""  # Comma-separated lane names to disable, e.g. "SIMPLE_TOOL,WORKFLOW"

    def _default_runtime_dir(self, name: str) -> str:
        if os.getenv("VERCEL"):
            return str(Path("/tmp") / name)
        return f"./{name}"

    def _first_env(self, *names: str) -> tuple[str, str]:
        for name in names:
            value = os.getenv(name, "").strip()
            if value:
                return value, name
        return "", ""

    def _json_env(self, name: str) -> dict:
        value = os.getenv(name, "").strip()
        if not value:
            return {}
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}

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
        database_url, database_url_source = self._first_env("DATABASE_URL")
        self.database_url = database_url or "postgresql://ai_hiking:ai_hiking@localhost:5432/ai_hiking"
        self.database_url_source = database_url_source if database_url else "local_default"
        database_timeout_fallback = "10" if os.getenv("VERCEL") else "2"
        self.database_connect_timeout_seconds = int(os.getenv("DATABASE_CONNECT_TIMEOUT_SECONDS", database_timeout_fallback))
        redis_url, redis_url_source = self._first_env(
            "REDIS_URL",
            "KV_URL",
            "UPSTASH_REDIS_URL",
        )
        redis_fallback = "" if os.getenv("VERCEL") else "redis://localhost:6379/0"
        self.redis_url = redis_url or redis_fallback
        self.redis_url_source = redis_url_source if redis_url else ("local_default" if redis_fallback else "")
        self.redis_rest_url, self.redis_rest_url_source = self._first_env(
            "UPSTASH_REDIS_REST_URL",
            "KV_REST_API_URL",
        )
        self.redis_rest_token, self.redis_rest_token_source = self._first_env(
            "UPSTASH_REDIS_REST_TOKEN",
            "KV_REST_API_TOKEN",
        )
        self.rag_docs_api_url = os.getenv("RAG_DOCS_API_URL", "")
        self.feishu_app_id = os.getenv("FEISHU_APP_ID", "")
        self.feishu_app_secret = os.getenv("FEISHU_APP_SECRET", "")
        self.feishu_default_space_id = os.getenv("FEISHU_DEFAULT_SPACE_ID", "")
        self.feishu_default_folder_token = os.getenv("FEISHU_DEFAULT_FOLDER_TOKEN", "")
        self.memory_store_path = os.getenv("MEMORY_STORE_PATH", self._default_runtime_dir("memory_store"))
        self.memory_top_k = int(os.getenv("MEMORY_TOP_K", "5"))
        self.memory_compressor_model = os.getenv("MEMORY_COMPRESSOR_MODEL", "deepseek-v4-flash")
        self.memory_extractor_model = os.getenv("MEMORY_EXTRACTOR_MODEL", "deepseek-v4-flash")
        self.memory_enabled = os.getenv("MEMORY_ENABLED", "true").lower() == "true"
        self.amap_api_key = os.getenv("AMAP_API_KEY", "")
        self.mcp_servers = self._json_env("MCP_SERVERS")
        self.mcp_capability_map = self._json_env("MCP_CAPABILITY_MAP")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY", "")
        self.disabled_lanes = os.getenv("DISABLED_LANES", "")

        return self

    @property
    def redis_connection_mode(self) -> str:
        if self.redis_url:
            return "redis_url"
        if self.redis_rest_url and self.redis_rest_token:
            return "upstash_rest"
        if self.redis_rest_url or self.redis_rest_token:
            return "incomplete_upstash_rest"
        return "none"

    @property
    def redis_configured(self) -> bool:
        return self.redis_connection_mode in {"redis_url", "upstash_rest"}

    @property
    def postgres_configured(self) -> bool:
        return self.database_url_source == "DATABASE_URL"

    @property
    def feishu_enabled(self) -> bool:
        return bool(self.feishu_app_id and self.feishu_app_secret)

    @property
    def feishu_default_configured(self) -> bool:
        return bool(self.feishu_default_space_id or self.feishu_default_folder_token)


settings = Settings().load()
