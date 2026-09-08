"""
ClimaX External Adapter Interfaces
Contracts for integrating third-party APIs and Google Cloud Services.
Implementations scheduled for Phase 3 (Data), Phase 5 (Gemini), and Phase 6 (Vertex).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IGCPStorageAdapter(ABC):
    @abstractmethod
    async def generate_signed_upload_url(self, file_path: str, content_type: str) -> str:
        pass


class IGeminiVisionAdapter(ABC):
    @abstractmethod
    async def analyze_multimodal_incident(self, media_uri: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        pass


class IVertexAIPredictionAdapter(ABC):
    @abstractmethod
    async def query_plume_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        pass


class IEarthEngineAdapter(ABC):
    @abstractmethod
    async def fetch_sentinel5p_raster(self, bbox: List[float], date_range: List[str]) -> Dict[str, Any]:
        pass


class IWeatherAdapter(ABC):
    @abstractmethod
    async def get_current_meteorology(self, lat: float, lng: float) -> Dict[str, Any]:
        pass
