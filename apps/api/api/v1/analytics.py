"""
Analytics API Router — /api/v1/analytics
Boundary for historical aggregations, BigQuery data explorer queries, and spatial trends.
Implementation scheduled for Phase 3 and Phase 13.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.base import ApiResponse

router = APIRouter(prefix="/analytics", tags=["Analytics & Research"])


@router.get("/summary", response_model=ApiResponse[dict], summary="Get macro environmental intelligence summary")
async def get_analytics_summary():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Analytics engine implementation begins in Phase 3."
    )
