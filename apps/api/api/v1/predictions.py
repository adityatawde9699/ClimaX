from fastapi import APIRouter, Depends, HTTPException, Query
from integrations.cache import cache
from repositories.predictions import PredictionRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from models.entities import Prediction
from schemas.base import ApiResponse, PaginatedResponse
from services.prediction_service import PredictionService

router = APIRouter(prefix="/predictions", tags=["Predictions"])


def serialize_prediction(item: Prediction) -> dict:
    return {
        "id": item.id,
        "latitude": item.latitude,
        "longitude": item.longitude,
        "horizon_hours": item.horizon_hours,
        "forecast_timestamp": item.forecast_timestamp,
        "predicted_aqi": item.predicted_aqi,
        "predicted_pm25": item.predicted_pm25,
        "confidence_interval_low": item.confidence_interval_low,
        "confidence_interval_high": item.confidence_interval_high,
        "tier": item.tier,
        "explanation": item.explanation,
    }


@router.get("", response_model=PaginatedResponse[dict])
async def list_predictions(
    lat: float = Query(...),
    lng: float = Query(...),
    horizon_hours: int = Query(24),
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"predictions:{round(lat, 4)}:{round(lng, 4)}:{horizon_hours}"
    cached = await cache.get(cache_key)
    if cached is not None:
        return PaginatedResponse(data=cached, total=len(cached))
    data = (
        await db.scalars(
            select(Prediction)
            .where(Prediction.horizon_hours == horizon_hours)
            .order_by(Prediction.created_at.desc())
            .limit(100)
        )
    ).all()
    if not data:
        try:
            data = await PredictionService(PredictionRepository(db)).generate_forecast(
                lat, lng, [horizon_hours]
            )
        except RuntimeError as exc:
            raise HTTPException(503, "Prediction provider is not configured or unavailable") from exc
    serialized = [serialize_prediction(item) for item in data]
    await cache.set(cache_key, serialized, settings.PREDICTION_CACHE_TTL_SECONDS)
    return PaginatedResponse(data=serialized, total=len(serialized))


@router.get("/{prediction_id}", response_model=ApiResponse[dict])
async def get_prediction(prediction_id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Prediction, prediction_id)
    if item is None:
        raise HTTPException(404, "Prediction not found")
    return ApiResponse(
        data={
            "id": item.id,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "horizon_hours": item.horizon_hours,
            "predicted_aqi": item.predicted_aqi,
            "tier": item.tier,
        }
    )
