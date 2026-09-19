from datetime import UTC, datetime, timedelta
from uuid import uuid4

from repositories.alerts import AlertRepository
from sqlalchemy import select

from models.entities import Alert
from schemas.entities import AlertChannel, AlertCreate


class AlertService:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def create_and_dispatch(self, payload: AlertCreate) -> Alert:
        data = payload.model_dump()
        data.update(
            id=str(uuid4()),
            severity=payload.severity.value,
            channel=payload.channel.value,
            is_dispatched=True,
            dispatched_at=datetime.now(UTC),
        )
        return await self.repository.create(data)

    async def dispatch(self, alert_id: str) -> Alert | None:
        return await self.repository.update(
            alert_id,
            {"is_dispatched": True, "dispatched_at": datetime.now(UTC)},
        )

    async def create_pm25_threshold_alert(
        self,
        *,
        sensor_id: str,
        pm25: float,
        affected_radius_m: float = 5000,
    ) -> Alert | None:
        """Create one active in-app threshold alert per sensor and severity per four hours."""
        severity = self.severity_for_pm25(pm25)
        if severity is None:
            return None

        now = datetime.now(UTC)
        title = f"PM2.5 threshold exceeded at sensor {sensor_id}"
        existing = await self.repository.session.scalar(
            select(Alert).where(
                Alert.title == title,
                Alert.severity == severity,
                Alert.channel == AlertChannel.IN_APP.value,
                Alert.created_at >= now - timedelta(hours=4),
                (Alert.expires_at.is_(None)) | (Alert.expires_at > now),
            )
        )
        if existing is not None:
            return None

        return await self.repository.create(
            {
                "id": str(uuid4()),
                "title": title,
                "message": (
                    f"PM2.5 reached {pm25:.1f} µg/m³. Follow local health guidance "
                    "and reduce outdoor exposure in the affected area."
                ),
                "severity": severity,
                "channel": AlertChannel.IN_APP.value,
                "affected_radius_m": affected_radius_m,
                "is_dispatched": True,
                "dispatched_at": now,
                "expires_at": now + timedelta(hours=4),
            }
        )

    @staticmethod
    def severity_for_pm25(pm25: float) -> str | None:
        if pm25 > 250:
            return "CRITICAL"
        if pm25 > 150:
            return "VERY_HIGH"
        return None
