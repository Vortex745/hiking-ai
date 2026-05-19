import asyncio
import json
import logging
import uuid
from typing import Optional

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from config import settings
from rag.text_processing import bm25_rank, reciprocal_rank_fusion

logger = logging.getLogger("ai-service.rag")


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class _PGVectorClient:
    """Lightweight pgvector client using psycopg (sync), no async needed."""

    def __init__(self, db_url: str):
        self._db_url = db_url
        self._conn = None
        self._ensure_table()

    def _get_conn(self):
        if self._conn is None or self._conn.closed:
            import psycopg
            self._conn = psycopg.connect(self._db_url, connect_timeout=2)
            self._conn.autocommit = True
        return self._conn

    def _ensure_table(self):
        conn = self._get_conn()
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rag_documents (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector,
                metadata JSONB DEFAULT '{}'
            )
        """)
        logger.info("pgvector table ensured (dynamic dimensions)")

    def add_documents(self, docs: list[Document], embeddings: list[list[float]]):
        conn = self._get_conn()
        for doc, emb in zip(docs, embeddings):
            doc_id = doc.metadata.get("id") or str(uuid.uuid4())
            meta = doc.metadata or {}
            # Remove embedding from metadata to keep it clean
            meta.pop("embedding", None)
            conn.execute(
                """
                INSERT INTO rag_documents (id, content, embedding, metadata)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    content = EXCLUDED.content,
                    embedding = EXCLUDED.embedding,
                    metadata = EXCLUDED.metadata
                """,
                (doc_id, doc.page_content, json.dumps(emb), json.dumps(meta, ensure_ascii=False)),
            )

    def similarity_search(self, query_embedding: list[float], k: int = 4) -> list[tuple[str, str, dict, float]]:
        conn = self._get_conn()
        query_dimensions = len(query_embedding)
        rows = conn.execute(
            """
            SELECT id, content, metadata,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM rag_documents
            WHERE embedding IS NOT NULL
              AND vector_dims(embedding) = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (json.dumps(query_embedding), query_dimensions, json.dumps(query_embedding), k),
        ).fetchall()
        return [(r[0], r[1], r[2], r[3]) for r in rows]

    def list_documents(self, status_filter: Optional[str] = None, limit: int = 5000) -> list[Document]:
        conn = self._get_conn()
        if status_filter:
            rows = conn.execute(
                """
                SELECT id, content, metadata
                FROM rag_documents
                WHERE metadata->>'status' = %s
                LIMIT %s
                """,
                (status_filter, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, content, metadata
                FROM rag_documents
                LIMIT %s
                """,
                (limit,),
            ).fetchall()

        docs: list[Document] = []
        for row_id, content, metadata in rows:
            if isinstance(metadata, str):
                metadata = json.loads(metadata)
            docs.append(Document(page_content=content, metadata={**(metadata or {}), "id": row_id}))
        return docs

    def has_documents(self, status_filter: Optional[str] = None) -> bool:
        conn = self._get_conn()
        if status_filter:
            row = conn.execute(
                """
                SELECT 1
                FROM rag_documents
                WHERE embedding IS NOT NULL
                  AND metadata->>'status' = %s
                LIMIT 1
                """,
                (status_filter,),
            ).fetchone()
        else:
            row = conn.execute(
                """
                SELECT 1
                FROM rag_documents
                WHERE embedding IS NOT NULL
                LIMIT 1
                """
            ).fetchone()
        return row is not None

    def document_count(self) -> int:
        conn = self._get_conn()
        row = conn.execute("SELECT COUNT(*) FROM rag_documents WHERE embedding IS NOT NULL").fetchone()
        return row[0] if row else 0

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()


class VectorStoreRetriever:
    """Vector store retriever using LangChain VectorStore abstraction.

    Uses InMemoryVectorStore for local dev/fallback,
    PGVector for production when database is available.
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        dimensions: int | None = None,
    ):
        self.embedding_base_url = base_url if base_url is not None else settings.embedding_base_url
        self.embedding_api_key = api_key if api_key is not None else settings.embedding_api_key
        self.embedding_model = model if model is not None else settings.embedding_model
        self.embedding_dimensions = dimensions if dimensions is not None else settings.embedding_dimensions

        self.embeddings: OpenAIEmbeddings | None = None
        self._store: InMemoryVectorStore | None = None
        self._pg_client: _PGVectorClient | None = None
        self._fallback_mode = True
        self._fallback_docs: list[Document] = []

        if self.embedding_api_key:
            self.embeddings = OpenAIEmbeddings(
                base_url=self.embedding_base_url,
                api_key=self.embedding_api_key,
                model=self.embedding_model,
            )

        self._try_connect_pgvector()

    def _try_connect_pgvector(self):
        """Try to connect to pgvector, fall back to in-memory."""
        if self.embeddings is None:
            logger.info("No embeddings configured, using in-memory store")
            self._store = InMemoryVectorStore(embedding=None)
            return

        try:
            self._pg_client = _PGVectorClient(settings.database_url)
            count = self._pg_client.document_count()
            self._fallback_mode = False
            logger.info("Connected to pgvector, %d documents in store", count)
        except Exception as e:
            logger.warning("pgvector connection failed, using InMemoryVectorStore: %s", e)
            self._pg_client = None
            self._fallback_mode = True
            self._store = InMemoryVectorStore(embedding=self.embeddings)

    @property
    def storage_mode(self) -> str:
        return "memory" if self._fallback_mode else "pgvector"

    def _embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts using the configured embedding model."""
        return self.embeddings.embed_documents(texts)

    def _embed_query(self, query: str) -> list[float]:
        """Embed a single query."""
        return self.embeddings.embed_query(query)

    def add_documents(self, docs: list[Document], status: Optional[str] = None):
        """Add documents with optional status metadata."""
        for doc in docs:
            if status:
                doc.metadata["status"] = status
        self._fallback_docs.extend(docs)

        if not self._fallback_mode and self._pg_client is not None:
            try:
                texts = [doc.page_content for doc in docs]
                embs = self._embed_texts(texts)
                self._pg_client.add_documents(docs, embs)
                return
            except Exception as e:
                logger.warning("pgvector add failed, falling back to memory: %s", e)
                self._fallback_mode = True
                if self._store is None:
                    self._store = InMemoryVectorStore(embedding=self.embeddings)

        if self._store is not None:
            try:
                self._store.add_documents(docs)
            except Exception as e:
                logger.warning("InMemoryVectorStore add failed: %s", e)
                if not hasattr(self, '_fallback_docs'):
                    self._fallback_docs = []
                self._fallback_docs.extend(docs)

    def similarity_search(self, query: str, k: int = 4, status_filter: Optional[str] = None) -> list[Document]:
        """Search for similar documents."""
        if self.embeddings is None:
            logger.warning("Embedding API key missing; returning no RAG matches")
            return []

        # Try pgvector first
        if not self._fallback_mode and self._pg_client is not None:
            try:
                if status_filter and not self._pg_client.has_documents(status_filter):
                    return []
                query_emb = self._embed_query(query)
                rows = self._pg_client.similarity_search(query_emb, k=k * 2)
                docs = [
                    Document(
                        page_content=content,
                        metadata=meta,
                    )
                    for _id, content, meta, _sim in rows
                ]
                return self._apply_status_filter(docs, status_filter)[:k]
            except Exception as e:
                logger.warning("pgvector vector search failed, continuing with lexical retrieval: %s", e)
                return []

        # InMemoryVectorStore search
        if self._store is not None:
            try:
                results = self._store.similarity_search(query, k=k * 2)
                return self._apply_status_filter(results, status_filter)[:k]
            except Exception as e:
                logger.warning("InMemoryVectorStore search failed: %s", e)

        # Fallback: simple list search
        if self._fallback_docs:
            return self._apply_status_filter(self._fallback_docs, status_filter)[:k]

        return []

    def bm25_search(self, query: str, k: int = 4, status_filter: Optional[str] = None) -> list[Document]:
        """Search documents with BM25 lexical scoring."""
        docs = self._all_documents(status_filter=status_filter)
        ranked = bm25_rank(query, docs, k=k)
        results: list[Document] = []
        for rank, (doc, score) in enumerate(ranked, start=1):
            results.append(Document(
                page_content=doc.page_content,
                metadata={
                    **(doc.metadata or {}),
                    "bm25_rank": rank,
                    "bm25_score": score,
                    "retrieval_method": "bm25",
                },
            ))
        return results

    def hybrid_search(self, queries: list[str], k: int = 4, status_filter: Optional[str] = None) -> list[Document]:
        """Run vector + BM25 retrieval for each query and fuse with RRF."""
        rank_lists: list[list[Document]] = []

        for query in queries:
            vector_docs = self.similarity_search(query, k=k, status_filter=status_filter)
            if vector_docs:
                rank_lists.append(vector_docs)

            bm25_docs = self.bm25_search(query, k=k, status_filter=status_filter)
            if bm25_docs:
                rank_lists.append(bm25_docs)

        return reciprocal_rank_fusion(rank_lists, k=k)

    def _all_documents(self, status_filter: Optional[str] = None) -> list[Document]:
        if not self._fallback_mode and self._pg_client is not None:
            try:
                return self._pg_client.list_documents(status_filter=status_filter)
            except Exception as e:
                logger.warning("pgvector document listing failed: %s", e)

        return self._apply_status_filter(self._fallback_docs, status_filter)

    @staticmethod
    def _apply_status_filter(docs: list[Document], status_filter: Optional[str] = None) -> list[Document]:
        """Filter documents by status metadata."""
        if not status_filter:
            return docs
        return [doc for doc in docs if doc.metadata.get("status") == status_filter]
