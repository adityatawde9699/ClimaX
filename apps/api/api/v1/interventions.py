from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from security.jwt import require_roles
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import Intervention, User
from schemas.base import ApiResponse
from schemas.entities import InterventionCreate, InterventionRead
from services.measurement_service import MeasurementService

router = APIRouter(prefix="/interventions", tags=["Interventions & Impact"])


class InterventionStatus(BaseModel):
    status: str


@router.post("/", response_model=ApiResponse[InterventionRead])
async def record_intervention(
    payload: InterventionCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    item = Intervention(id=str(uuid4()), **payload.model_dump(), dispatched_at=datetime.now(UTC))
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ApiResponse(data=item)


@router.patch("/{intervention_id}/status", response_model=ApiResponse[InterventionRead])
async def update_intervention(
    intervention_id: str,
    payload: InterventionStatus,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    item = await db.get(Intervention, intervention_id)
    if item is None:
        raise HTTPException(404, "Intervention not found")
    now = datetime.now(UTC)
    if payload.status == "EXECUTED":
        item.executed_at = now
    elif payload.status == "COMPLETED":
        item.completed_at = now
    else:
        raise HTTPException(422, "Status must be EXECUTED or COMPLETED")
    await db.commit()
    if payload.status == "COMPLETED":
        await MeasurementService().record(db, item.id, 100.0, 85.0)
    await db.refresh(item)
    return ApiResponse(data=item)


@router.patch("/{intervention_id}/complete", response_model=ApiResponse[InterventionRead])
async def complete_intervention(
    intervention_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    return await update_intervention(
        intervention_id, InterventionStatus(status="COMPLETED"), db, user
    )
