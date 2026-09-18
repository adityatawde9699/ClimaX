from datetime import UTC, datetime

from events.broker import broker
from fastapi import APIRouter, Depends, HTTPException
from repositories.alerts import AlertRepository
from security.jwt import require_roles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import Alert, User
from schemas.base import ApiResponse, PaginatedResponse
from schemas.entities import AlertCreate, AlertRead
from services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts & Advisories"])


@router.get("/", response_model=PaginatedResponse[AlertRead])
async def list_alerts(
    severity: str | None = None, active: bool = True, db: AsyncSession = Depends(get_db)
):
    statement = select(Alert)
    if severity:
        statement = statement.where(Alert.severity == severity)
    if active:
        statement = statement.where(
            (Alert.expires_at.is_(None)) | (Alert.expires_at > datetime.now(UTC))
        )
    data = (await db.scalars(statement.order_by(Alert.created_at.desc()))).all()
    return PaginatedResponse(data=data, total=len(data))


@router.post("/", response_model=ApiResponse[AlertRead])
async def broadcast_alert(
    payload: AlertCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    item = await AlertService(AlertRepository(db)).create_and_dispatch(payload)
    await db.commit()
    await db.refresh(item)
    await broker.publish("alert.dispatched", {"id": item.id, "severity": item.severity})
    return ApiResponse(data=item)


@router.get("/{alert_id}", response_model=ApiResponse[AlertRead])
async def get_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    item = await db.get(Alert, alert_id)
    if item is None:
        raise HTTPException(404, "Alert not found")
    return ApiResponse(data=item)


@router.post("/{alert_id}/dispatch", response_model=ApiResponse[AlertRead])
async def dispatch_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    item = await AlertService(AlertRepository(db)).dispatch(alert_id)
    if item is None:
        raise HTTPException(404, "Alert not found")
    await db.commit()
    await db.refresh(item)
    await broker.publish("alert.dispatched", {"id": item.id, "severity": item.severity})
    return ApiResponse(data=item)
