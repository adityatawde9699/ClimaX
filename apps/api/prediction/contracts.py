"""
ClimaX Predictive Modeling Interfaces
Contract for 6h-72h atmospheric forecasting and plume dispersion models.
"""

from abc import ABC, abstractmethod
from typing import Any

from schemas.entities import PredictionRead


class IPollutionPredictor(ABC):
    """Predicts future AQI and pollutant concentrations across spatio-temporal grids."""

    @abstractmethod
    async def predict_aqi_timeline(
        self, latitude: float, longitude: float, horizon_hours: list[int]
    ) -> list[PredictionRead]:
        pass

    @abstractmethod
    async def simulate_plume_dispersion(
        self,
        source_coordinates: dict[str, float],
        emission_rate: float,
        wind_speed: float,
        wind_direction: float,
    ) -> dict[str, Any]:
        pass
