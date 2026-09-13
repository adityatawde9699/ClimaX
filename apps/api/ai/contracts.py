"""
ClimaX AI Orchestration Interfaces
Defines contracts for Gemini Multimodal processing, Environmental Reasoning, and AI Copilot.
"""

from abc import ABC, abstractmethod
from typing import Any

from schemas.ai import AIExplanationSchema


class IMultimodalReportAnalyzer(ABC):
    """Orchestrates citizen photo/video classification via Gemini 1.5."""

    @abstractmethod
    async def analyze(
        self, image_bytes: bytes, latitude: float, longitude: float, citizen_text: str
    ) -> AIExplanationSchema:
        pass


class IEnvironmentalReasoningEngine(ABC):
    """Reasoning engine synthesizing multi-sensor spikes and wind data into root-cause explanations."""

    @abstractmethod
    async def reason_about_hotspot(
        self,
        sensor_data: dict[str, Any],
        wind_vector: dict[str, Any],
        nearby_industries: dict[str, Any],
    ) -> AIExplanationSchema:
        pass


class IAICopilotService(ABC):
    """Interactive conversational agent for municipal authorities and citizens."""

    @abstractmethod
    async def answer_query(
        self, session_id: str, user_role: str, query: str, context_data: dict[str, Any]
    ) -> dict[str, Any]:
        pass
