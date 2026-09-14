from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

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
    return ApiResponse(data=serialize(await RiskService().evaluate(db, lat, lng)))


@router.get("/hotspots", response_model=PaginatedResponse[dict])
async def hotspots(db: AsyncSession = Depends(get_db)):
    data = (
        await db.scalars(select(RiskAssessment).order_by(desc(RiskAssessment.risk_score)).limit(10))
    ).all()
    return PaginatedResponse(data=[serialize(item) for item in data], total=len(data))
