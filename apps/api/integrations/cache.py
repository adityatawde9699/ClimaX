"""Best-effort Redis JSON cache used by read-heavy API routes."""

import json
from datetime import date, datetime
from typing import Any

from core.config import settings


def _json_default(value: Any) -> str:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    raise TypeError(f"Cannot serialize {type(value).__name__}")


class RedisJsonCache:
    async def get(self, key: str) -> Any | None:
        client = None
        try:
            import redis.asyncio as redis

            client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            value = await client.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None
        finally:
            if client is not None:
                await client.aclose()

    async def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        client = None
        try:
            import redis.asyncio as redis

            client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await client.set(key, json.dumps(value, default=_json_default), ex=ttl_seconds)
        except Exception:
            return
        finally:
            if client is not None:
                await client.aclose()

    async def delete_pattern(self, pattern: str) -> None:
        client = None
        try:
            import redis.asyncio as redis

            client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            keys = [key async for key in client.scan_iter(match=pattern, count=100)]
            if keys:
                await client.delete(*keys)
        except Exception:
            return
        finally:
            if client is not None:
                await client.aclose()


cache = RedisJsonCache()
