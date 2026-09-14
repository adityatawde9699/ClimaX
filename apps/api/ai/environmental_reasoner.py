"""Post-analysis contextual reasoning for incident root causes."""

from ai.contracts import IEnvironmentalReasoningEngine
from integrations.gemini_adapter import GeminiAdapter

from schemas.ai import AIExplanationSchema, ConfidenceTier


class EnvironmentalReasoningEngine(IEnvironmentalReasoningEngine):
    def __init__(self, gemini: GeminiAdapter | None = None):
        self.gemini = gemini or GeminiAdapter()

    async def reason_about_hotspot(
        self, sensor_data: dict, wind_vector: dict, nearby_industries: dict
    ) -> AIExplanationSchema:
        prompt = f"Assess likely pollution root cause using sensors={sensor_data}, wind={wind_vector}, sources={nearby_industries}. Return concise JSON with result and reasoning_steps."
        raw, _ = await self.gemini.generate([prompt])
        return AIExplanationSchema(
            result=raw,
            confidence=0.6,
            confidence_tier=ConfidenceTier.MEDIUM,
            evidence=["Sensor and wind context synthesized"],
            reasoning_steps=["Compared local readings with wind direction"],
            data_sources=["environmental_observations"],
            model=self.gemini.model_name,
        )
