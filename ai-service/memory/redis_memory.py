import json
import logging
from typing import Optional

from config import settings
from memory.base import ChatMemory

logger = logging.getLogger("ai-service.memory")
WINDOW_SIZE = 20

try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("redis-py not installed, RedisChatMemory will raise ImportError on use")


class RedisChatMemory(ChatMemory):
    """Redis-based chat memory with sliding window.

    Uses async Redis operations. When called synchronously from sync code,
    wraps calls with asyncio.run().
    """

    def __init__(self, chat_id: str = "default"):
        self.chat_id = chat_id
        self.redis_key = f"chat:{chat_id}:messages"
        self._client: Optional[aioredis.Redis] = None

    async def _ensure_client(self):
        if self._client is None:
            if not REDIS_AVAILABLE:
                raise ImportError("redis[asyncio] is required for RedisChatMemory. Install with: pip install redis")
            self._client = aioredis.from_url(settings.redis_url, decode_responses=True)
        return self._client

    def add_message(self, role: str, content: str):
        """Add a message synchronously."""
        import asyncio
        return asyncio.run(self._add_message_async(role, content))

    async def _add_message_async(self, role: str, content: str):
        client = await self._ensure_client()
        msg = json.dumps({"role": role, "content": content}, ensure_ascii=False)
        await client.rpush(self.redis_key, msg)
        await client.ltrim(self.redis_key, -WINDOW_SIZE, -1)

    def get_messages(self) -> list[dict]:
        """Get all messages synchronously."""
        import asyncio
        return asyncio.run(self._get_messages_async())

    async def _get_messages_async(self) -> list[dict]:
        client = await self._ensure_client()
        raw_messages = await client.lrange(self.redis_key, 0, -1)
        messages = []
        for raw in raw_messages:
            try:
                messages.append(json.loads(raw))
            except json.JSONDecodeError:
                continue
        return messages

    def clear(self):
        """Clear all messages synchronously."""
        import asyncio
        return asyncio.run(self._clear_async())

    async def _clear_async(self):
        client = await self._ensure_client()
        await client.delete(self.redis_key)
