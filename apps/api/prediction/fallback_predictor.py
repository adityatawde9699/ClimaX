from datetime import UTC, datetime

from prediction.gaussian_plume import plume_geojson


class FallbackPredictor:
    async def predict(
        self,
        latitude: float,
        longitude: float,
        horizon_hours: int,
        pm25: float = 80,
        wind_speed: float = 10,
        wind_direction: float = 90,
    ) -> dict:
        factor = 1 + (horizon_hours / 72) * 0.25 - min(wind_speed, 30) / 200
        predicted_pm25 = max(1.0, pm25 * factor)
        return {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_timestamp": datetime.now(UTC),
            "horizon_hours": horizon_hours,
            "predicted_pm25": predicted_pm25,
            "predicted_aqi": min(500.0, predicted_pm25 * 1.5),
            "confidence_interval_low": predicted_pm25 * 0.75,
            "confidence_interval_high": predicted_pm25 * 1.25,
            "explanation": {
                "result": "Physics-informed Gaussian plume fallback",
                "confidence": 0.55,
                "confidence_tier": "LOW",
                "evidence": ["Wind-adjusted local PM2.5"],
                "data_sources": ["fallback"],
                "model": "gaussian-plume",
            },
            "plume": plume_geojson(latitude, longitude, wind_speed, wind_direction),
        }
