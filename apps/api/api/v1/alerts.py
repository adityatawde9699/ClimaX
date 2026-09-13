from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends
from security.jwt import require_roles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import Alert, User
from schemas.base import ApiResponse, PaginatedResponse
from schemas.entities import AlertCreate, AlertRead

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
    data = (await db.scalars(statement)).all()
    return PaginatedResponse(data=data, total=len(data))


@router.post("/", response_model=ApiResponse[AlertRead])
async def broadcast_alert(
    payload: AlertCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("AUTHORITY", "ADMIN")),
):
    values = payload.model_dump()
    values.update(severity=payload.severity.value, channel=payload.channel.value)
    item = Alert(
        id=str(uuid4()),
        **values,
        is_dispatched=True,
        dispatched_at=datetime.now(UTC),
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ApiResponse(data=item)
