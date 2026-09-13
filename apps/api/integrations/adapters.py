"""
ClimaX External Adapter Interfaces
Contracts for integrating third-party APIs and Google Cloud Services.
Implementations scheduled for Phase 3 (Data), Phase 5 (Gemini), and Phase 6 (Vertex).
"""

from abc import ABC, abstractmethod
from typing import Any


class IGCPStorageAdapter(ABC):
    @abstractmethod
    async def generate_signed_upload_url(self, file_path: str, content_type: str) -> str:
        pass


class IGeminiVisionAdapter(ABC):
    @abstractmethod
    async def analyze_multimodal_incident(
        self, media_uri: str, metadata: dict[str, Any]
    ) -> dict[str, Any]:
        pass


class IVertexAIPredictionAdapter(ABC):
    @abstractmethod
    async def query_plume_prediction(self, features: dict[str, Any]) -> dict[str, Any]:
        pass


class IEarthEngineAdapter(ABC):
    @abstractmethod
    async def fetch_sentinel5p_raster(
        self, bbox: list[float], date_range: list[str]
    ) -> dict[str, Any]:
        pass


class IWeatherAdapter(ABC):
    @abstractmethod
    async def get_current_meteorology(self, lat: float, lng: float) -> dict[str, Any]:
        pass
