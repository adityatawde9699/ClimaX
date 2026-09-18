from fastapi import APIRouter, Depends, Query
from integrations.cache import cache
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from models.entities import RiskAssessment
from schemas.base import ApiResponse, PaginatedResponse
from services.risk_service import RiskService

router = APIRouter(prefix="/risk", tags=["Environmental Risk"])


def serialize(item):
    return {
        "id": item.id,
        "location": {"latitude": item.latitude, "longitude": item.longitude},
        "risk_score": item.risk_score,
        "severity": item.severity,
        "population_vulnerability_index": item.population_vulnerability_index,
        "sensitive_receptors_count": item.sensitive_receptors_count,
        "dominant_pollutant": item.dominant_pollutant,
        "calculated_at": item.calculated_at,
    }


@router.get("", response_model=ApiResponse[dict])
async def evaluate_risk(
    lat: float = Query(...), lng: float = Query(...), db: AsyncSession = Depends(get_db)
):
    cache_key = f"risk:{round(lat, 4)}:{round(lng, 4)}"
    cached = await cache.get(cache_key)
    if cached is not None:
        return ApiResponse(data=cached)
    data = serialize(await RiskService().evaluate(db, lat, lng))
    await cache.set(cache_key, data, settings.RISK_CACHE_TTL_SECONDS)
    return ApiResponse(data=data)


@router.get("/hotspots", response_model=PaginatedResponse[dict])
async def hotspots(db: AsyncSession = Depends(get_db)):
    cached = await cache.get("risk:hotspots")
    if cached is not None:
        return PaginatedResponse(data=cached, total=len(cached))
    data = (
        await db.scalars(select(RiskAssessment).order_by(desc(RiskAssessment.risk_score)).limit(10))
    ).all()
    serialized = [serialize(item) for item in data]
    await cache.set("risk:hotspots", serialized, settings.RISK_CACHE_TTL_SECONDS)
    return PaginatedResponse(data=serialized, total=len(serialized))
