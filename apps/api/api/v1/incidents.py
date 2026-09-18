"""
Incidents API Router — /api/v1/incidents
Boundary for environmental incident triage, field dispatch, and status lifecycle.
Implementation scheduled for Phase 9.
"""

from datetime import UTC, datetime
from uuid import uuid4

from events.broker import broker
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from repositories.interventions import InterventionRepository
from security.jwt import require_roles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import Incident, User
from schemas.base import ApiResponse, PaginatedResponse
from schemas.entities import IncidentCreate, IncidentRead, InterventionCreate
from services.incident_service import can_transition
from services.intervention_service import InterventionService

router = APIRouter(prefix="/incidents", tags=["Incidents"])


def serialize(item: Incident) -> dict:
    return {
        "id": item.id,
        "organization_id": item.organization_id,
        "title": item.title,
        "status": item.status,
        "severity": item.severity,
        "category": item.category,
        "location": {"latitude": item.latitude, "longitude": item.longitude},
        "assigned_officer_id": item.assigned_officer_id,
        "risk_score": item.risk_score,
        "ai_analysis_id": item.ai_analysis_id,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "resolved_at": item.resolved_at,
    }


class StatusUpdate(BaseModel):
    status: str


class DispatchRequest(BaseModel):
    intervention_type: str
    executing_agency: str
    action_summary: str


@router.get("/", response_model=PaginatedResponse[IncidentRead], summary="List active incidents")
async def list_incidents(db: AsyncSession = Depends(get_db)):
    items = (await db.scalars(select(Incident))).all()
    return PaginatedResponse(data=[serialize(item) for item in items], total=len(items))


@router.get("/export/csv")
async def export_incidents(db: AsyncSession = Depends(get_db)):
    items = (await db.scalars(select(Incident))).all()
    rows = ["id,title,severity,status"] + [
        f'"{item.id}","{item.title}","{item.severity}","{item.status}"' for item in items
    ]
    return Response("\n".join(rows), media_type="text/csv")


@router.post("/", response_model=ApiResponse[IncidentRead], summary="Create new incident")
async def create_incident(
    incident: IncidentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    if not user.organization_id:
        raise HTTPException(422, "Authority must belong to an organization")
    item = Incident(
        id=str(uuid4()),
        organization_id=user.organization_id,
        title=incident.title,
        severity=incident.severity.value,
        category=incident.category.value,
        latitude=incident.location.latitude,
        longitude=incident.location.longitude,
        geom=f"SRID=4326;POINT({incident.location.longitude} {incident.location.latitude})",
        assigned_officer_id=incident.assigned_officer_id,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    await broker.publish("incident.created", serialize(item))
    return ApiResponse(data=serialize(item))


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(incident_id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Incident, incident_id)
    if item is None:
        raise HTTPException(404, "Incident not found")
    return serialize(item)


@router.patch("/{incident_id}/status", response_model=ApiResponse[IncidentRead])
async def update_status(
    incident_id: str,
    payload: StatusUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    item = await db.get(Incident, incident_id)
    if item is None:
        raise HTTPException(404, "Incident not found")
    try:
        valid = can_transition(item.status, payload.status)
    except ValueError:
        valid = False
    if not valid:
        raise HTTPException(409, f"Invalid transition from {item.status} to {payload.status}")
    item.status = payload.status
    if payload.status == "RESOLVED":
        item.resolved_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(item)
    await broker.publish("incident.updated", serialize(item))
    return ApiResponse(data=serialize(item))


@router.post("/{incident_id}/assign", response_model=ApiResponse[IncidentRead])
async def assign_incident(
    incident_id: str,
    officer_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    item = await db.get(Incident, incident_id)
    if item is None:
        raise HTTPException(404, "Incident not found")
    item.assigned_officer_id = officer_id
    await db.commit()
    await db.refresh(item)
    return ApiResponse(data=serialize(item))


@router.post("/{incident_id}/dispatch", response_model=ApiResponse[dict])
async def dispatch_incident_intervention(
    incident_id: str,
    payload: DispatchRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    incident = await db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(404, "Incident not found")
    if incident.status not in {"OPEN", "INVESTIGATING"}:
        raise HTTPException(409, f"Incident in {incident.status} cannot be dispatched")
    intervention = await InterventionService(InterventionRepository(db)).dispatch(
        InterventionCreate(incident_id=incident.id, **payload.model_dump())
    )
    incident.status = "DISPATCHED"
    await db.commit()
    await db.refresh(incident)
    await db.refresh(intervention)
    await broker.publish("incident.updated", serialize(incident))
    await broker.publish(
        "intervention.dispatched",
        {"id": intervention.id, "incident_id": incident.id},
    )
    return ApiResponse(data={"incident": serialize(incident), "intervention_id": intervention.id})
