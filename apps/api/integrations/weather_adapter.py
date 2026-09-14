"""Open-Meteo adapter with a small in-process one-hour location cache."""

import json
from datetime import UTC, datetime, timedelta

import httpx

from core.config import settings


class WeatherAdapter:
    _cache: dict[tuple[float, float], tuple[datetime, dict[str, float | None]]] = {}

    async def get_current_meteorology(
        self, latitude: float, longitude: float
    ) -> dict[str, float | None]:
        key = (round(latitude, 3), round(longitude, 3))
        redis_key = f"weather:{key[0]}:{key[1]}"
        try:
            import redis.asyncio as redis

            client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            cached_redis = await client.get(redis_key)
            await client.aclose()
            if cached_redis:
                return json.loads(cached_redis)
        except Exception:  # cache failures must not make the weather provider unavailable
            pass
        cached = self._cache.get(key)
        if cached and cached[0] > datetime.now(UTC):
            return cached[1]
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m",
        }
        async with httpx.AsyncClient(timeout=4.0) as client:
            response = await client.get(settings.OPEN_METEO_BASE_URL, params=params)
            response.raise_for_status()
        current = response.json().get("current", {})
        result = {
            "temperature_c": current.get("temperature_2m"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "wind_direction_deg": current.get("wind_direction_10m"),
        }
        self._cache[key] = (datetime.now(UTC) + timedelta(hours=1), result)
        try:
            import redis.asyncio as redis

            client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            await client.set(redis_key, json.dumps(result), ex=3600)
            await client.aclose()
        except Exception:  # cache failures must not make the weather provider unavailable
            pass
        return result
