from events.broker import broker
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from repositories.interventions import InterventionRepository
from security.jwt import require_roles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import Intervention, User
from schemas.base import ApiResponse, PaginatedResponse
from schemas.entities import InterventionCreate, InterventionRead
from services.intervention_service import InterventionService
from services.measurement_service import MeasurementService

router = APIRouter(prefix="/interventions", tags=["Interventions & Impact"])


class InterventionStatus(BaseModel):
    status: str


@router.get("/", response_model=PaginatedResponse[InterventionRead])
async def list_interventions(
    incident_id: str | None = None, db: AsyncSession = Depends(get_db)
):
    statement = select(Intervention).order_by(Intervention.dispatched_at.desc())
    if incident_id:
        statement = statement.where(Intervention.incident_id == incident_id)
    items = (await db.scalars(statement)).all()
    return PaginatedResponse(data=items, total=len(items))


@router.post("/", response_model=ApiResponse[InterventionRead])
async def record_intervention(
    payload: InterventionCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    item = await InterventionService(InterventionRepository(db)).dispatch(payload)
    await db.commit()
    await db.refresh(item)
    await broker.publish(
        "intervention.dispatched", {"id": item.id, "incident_id": item.incident_id}
    )
    return ApiResponse(data=item)


@router.get("/{intervention_id}", response_model=ApiResponse[InterventionRead])
async def get_intervention(intervention_id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Intervention, intervention_id)
    if item is None:
        raise HTTPException(404, "Intervention not found")
    return ApiResponse(data=item)


@router.patch("/{intervention_id}/status", response_model=ApiResponse[InterventionRead])
async def update_intervention(
    intervention_id: str,
    payload: InterventionStatus,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    try:
        item = await InterventionService(InterventionRepository(db)).update_status(
            intervention_id, payload.status
        )
    except ValueError:
        raise HTTPException(422, "Status must be EXECUTED or COMPLETED") from None
    if item is None:
        raise HTTPException(404, "Intervention not found")
    await db.commit()
    if payload.status == "COMPLETED":
        await MeasurementService().record_from_observations(db, item)
    await db.refresh(item)
    await broker.publish(
        "intervention.updated",
        {"id": item.id, "incident_id": item.incident_id, "status": payload.status},
    )
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
