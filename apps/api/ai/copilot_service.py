"""Role-aware Gemini copilot with bounded in-memory conversation history."""

from collections import defaultdict

from ai.contracts import IAICopilotService
from integrations.gemini_adapter import GeminiAdapter


class AICopilotService(IAICopilotService):
    def __init__(self, gemini: GeminiAdapter | None = None):
        self.gemini = gemini or GeminiAdapter()
        self.history: dict[str, list[dict[str, str]]] = defaultdict(list)

    async def answer_query(
        self, session_id: str, user_role: str, query: str, context_data: dict
    ) -> dict:
        history = self.history[session_id][-10:]
        guidance = (
            "tactical municipal recommendations"
            if user_role in {"AUTHORITY", "ADMIN"}
            else "clear health guidance for residents"
        )
        prompt = f"You are ClimaX Copilot. Give {guidance}. Platform context: {context_data}. Conversation: {history}. User: {query}"
        answer, tokens = await self.gemini.generate([prompt])
        history.extend(
            [{"role": "user", "content": query}, {"role": "assistant", "content": answer}]
        )
        self.history[session_id] = history[-10:]
        return {
            "answer": answer,
            "tier": "INFERRED",
            "model_version": self.gemini.model_name,
            "token_usage": tokens,
        }
