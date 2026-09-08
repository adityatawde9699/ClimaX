"""
Predictions API Router — /api/v1/predictions
Boundary for 6h, 24h, and 72h localized pollution predictions and dispersion forecasts.
Implementation scheduled for Phase 6.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.entities import PredictionRead
from schemas.base import ApiResponse, PaginatedResponse, CoordinatesDTO

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.post("/forecast", response_model=ApiResponse[PredictionRead], summary="Generate pollution forecast for coordinates")
async def get_forecast(location: CoordinatesDTO):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Predictive model integration begins in Phase 6."
    )
