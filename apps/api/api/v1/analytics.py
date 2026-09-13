from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import Alert, CitizenReport, EnvironmentalObservation, Incident, Intervention
from schemas.base import ApiResponse

router = APIRouter(prefix="/analytics", tags=["Analytics & Research"])


@router.get("/summary", response_model=ApiResponse[dict])
async def summary(db: AsyncSession = Depends(get_db)):
    async def count(model):
        return await db.scalar(select(func.count()).select_from(model)) or 0

    return ApiResponse(
        data={
            "observations": await count(EnvironmentalObservation),
            "reports": await count(CitizenReport),
            "incidents": await count(Incident),
            "alerts": await count(Alert),
            "interventions": await count(Intervention),
        }
    )


@router.get("/intervention-effectiveness", response_model=ApiResponse[dict])
async def intervention_effectiveness(db: AsyncSession = Depends(get_db)):
    completed = (
        await db.scalar(
            select(func.count())
            .select_from(Intervention)
            .where(Intervention.completed_at.is_not(None))
        )
        or 0
    )
    total = await db.scalar(select(func.count()).select_from(Intervention)) or 0
    return ApiResponse(
        data={
            "total": total,
            "completed": completed,
            "completion_rate": completed / total if total else 0,
        }
    )
