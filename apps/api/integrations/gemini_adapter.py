"""Resilient Gemini transport with bounded retries and token accounting."""

import asyncio
from collections.abc import Sequence
from typing import Any

from core.config import settings


class GeminiAdapter:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.GEMINI_MODEL_MULTIMODAL
        self.total_tokens = 0

    def _model(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise RuntimeError("google-generativeai must be installed") from exc
        genai.configure(api_key=settings.GEMINI_API_KEY)
        return genai.GenerativeModel(self.model_name)

    async def generate(self, parts: Sequence[Any]) -> tuple[str, int]:
        """Generate once successfully, retrying transient provider errors three times."""
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                response = await asyncio.wait_for(
                    asyncio.to_thread(self._model().generate_content, list(parts)), timeout=30
                )
                usage = getattr(response, "usage_metadata", None)
                tokens = int(getattr(usage, "total_token_count", 0) or 0)
                self.total_tokens += tokens
                return response.text, tokens
            except Exception as exc:
                last_error = exc
                if attempt < 2:
                    await asyncio.sleep(2**attempt)
        raise RuntimeError("Gemini request failed after three attempts") from last_error
