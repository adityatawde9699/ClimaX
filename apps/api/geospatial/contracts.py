"""
ClimaX Geospatial & PostGIS Query Interfaces
Handles spatial geometry operations, polygon clipping, and coordinate reference systems.
"""

from abc import ABC, abstractmethod
from typing import Any


class IGeospatialService(ABC):
    """Interface for PostGIS geospatial queries and buffer computations."""

    @abstractmethod
    def create_point_wkt(self, latitude: float, longitude: float) -> str:
        pass

    @abstractmethod
    def calculate_bounding_box(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[float]:
        pass

    @abstractmethod
    def buffer_polygon_meters(
        self, geojson_polygon: dict[str, Any], distance_m: float
    ) -> dict[str, Any]:
        pass
