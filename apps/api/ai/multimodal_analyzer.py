"""Gemini-backed structured analysis for citizen report media."""

import json
import re

from ai.contracts import IMultimodalReportAnalyzer
from integrations.gemini_adapter import GeminiAdapter

from schemas.ai import AIExplanationSchema, ConfidenceTier, PollutionCategory

SYSTEM_PROMPT = (
    "You are an environmental incident analyst. Return JSON only with pollution_category, "
    "suggested_severity, confidence, result, reasoning_steps, health_risk, and plume_bbox. "
    "Never claim certainty."
)


def _confidence_tier(confidence: float) -> ConfidenceTier:
    if confidence >= 0.95:
        return ConfidenceTier.CRITICAL
    if confidence >= 0.8:
        return ConfidenceTier.HIGH
    if confidence >= 0.6:
        return ConfidenceTier.MEDIUM
    return ConfidenceTier.LOW


class MultimodalReportAnalyzer(IMultimodalReportAnalyzer):
    def __init__(self, gemini: GeminiAdapter | None = None):
        self.gemini = gemini or GeminiAdapter()
        self.last_raw_response = ""

    async def analyze(
        self, image_bytes: bytes, latitude: float, longitude: float, citizen_text: str
    ) -> AIExplanationSchema:
        prompt = f"{SYSTEM_PROMPT} Location: {latitude},{longitude}. Citizen report: {citizen_text}"
        raw, _ = await self.gemini.generate(
            [prompt, {"mime_type": "image/jpeg", "data": image_bytes}]
        )
        self.last_raw_response = raw
        payload = self._extract_json(raw)
        confidence = max(0.0, min(float(payload.get("confidence", 0.35)), 1.0))
        try:
            category = PollutionCategory(payload.get("pollution_category", "OTHER"))
        except ValueError:
            category = PollutionCategory.OTHER
        steps = payload.get("reasoning_steps") or payload.get("evidence") or []
        return AIExplanationSchema(
            result=str(payload.get("result", "Potential environmental pollution observed.")),
            confidence=confidence,
            confidence_tier=_confidence_tier(confidence),
            evidence=list(steps),
            reasoning_steps=list(steps),
            data_sources=["citizen_report_media"],
            model=self.gemini.model_name,
            pollution_category=category,
            suggested_severity=str(payload.get("suggested_severity", "MODERATE")),
            plume_bbox=payload.get("plume_bbox"),
            health_risk=payload.get("health_risk"),
        )

    @staticmethod
    def _extract_json(raw: str) -> dict:
        candidate = raw.strip().removeprefix("```json").removesuffix("```").strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            matched = re.search(r"\{.*\}", raw, re.DOTALL)
            if matched:
                try:
                    return json.loads(matched.group())
                except json.JSONDecodeError:
                    pass
        return {}
