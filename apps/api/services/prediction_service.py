from uuid import uuid4

from integrations.vertex_adapter import VertexAdapter
from prediction.fallback_predictor import FallbackPredictor
from repositories.predictions import PredictionRepository

from models.entities import Prediction


class PredictionService:
    def __init__(self, repository: PredictionRepository):
        self.repository = repository
        self.fallback = FallbackPredictor()
        self.vertex = VertexAdapter()

    async def generate_forecast(
        self, latitude: float, longitude: float, horizons: list[int] | None = None
    ) -> list[Prediction]:
        horizons = horizons or [6, 24, 72]
        output = []
        for horizon in horizons:
            try:
                value = await self.vertex.query_plume_prediction(
                    {"latitude": latitude, "longitude": longitude, "horizon_hours": horizon}
                )
            except Exception:
                value = await self.fallback.predict(latitude, longitude, horizon)
            output.append(
                await self.repository.create(
                    {
                        "id": str(uuid4()),
                        "tier": "PREDICTED",
                        **{
                            key: value[key]
                            for key in (
                                "latitude",
                                "longitude",
                                "forecast_timestamp",
                                "horizon_hours",
                                "predicted_pm25",
                                "predicted_aqi",
                                "confidence_interval_low",
                                "confidence_interval_high",
                                "explanation",
                            )
                        },
                    }
                )
            )
        return output
