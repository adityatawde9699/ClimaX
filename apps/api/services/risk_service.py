from datetime import UTC, datetime
from uuid import uuid4

from events.broker import broker
from sqlalchemy import select

from core.config import settings
from models.entities import Incident, Organization, RiskAssessment


class RiskService:
    async def evaluate(
        self,
        session,
        latitude: float,
        longitude: float,
        aqi: float = 100,
        receptors: int = 0,
        population_density: float = 0.5,
    ) -> RiskAssessment:
        normalized = min(aqi / 500, 1)
        sensitivity = min(receptors / 10, 1)
        score = normalized * 0.4 + sensitivity * 0.35 + population_density * 0.25
        severity = (
            "CRITICAL"
            if score >= 0.8
            else "VERY_HIGH"
            if score >= 0.6
            else "HIGH"
            if score >= 0.4
            else "MODERATE"
        )
        item = RiskAssessment(
            id=str(uuid4()),
            latitude=latitude,
            longitude=longitude,
            risk_score=score,
            severity=severity,
            population_vulnerability_index=sensitivity,
            sensitive_receptors_count=receptors,
            calculated_at=datetime.now(UTC),
        )
        session.add(item)
        incident = await self._create_incident_for_extreme_risk(session, item)
        await session.commit()
        await session.refresh(item)
        if incident is not None:
            await broker.publish(
                "incident.created",
                {"id": incident.id, "severity": incident.severity, "risk_score": score},
            )
        return item

    async def _create_incident_for_extreme_risk(
        self, session, assessment: RiskAssessment
    ) -> Incident | None:
        organization_id = settings.RISK_AUTO_INCIDENT_ORGANIZATION_ID
        if assessment.severity not in {"VERY_HIGH", "CRITICAL"} or not organization_id:
            return None
        if await session.get(Organization, organization_id) is None:
            return None
        existing = await session.scalar(
            select(Incident).where(
                Incident.organization_id == organization_id,
                Incident.status.not_in(("RESOLVED", "DISMISSED")),
                Incident.category == "OTHER",
                Incident.latitude.between(assessment.latitude - 0.01, assessment.latitude + 0.01),
                Incident.longitude.between(
                    assessment.longitude - 0.01, assessment.longitude + 0.01
                ),
            )
        )
        if existing is not None:
            return None
        incident = Incident(
            id=str(uuid4()),
            organization_id=organization_id,
            title=f"Automatic {assessment.severity.lower().replace('_', ' ')} risk incident",
            status="OPEN",
            severity=assessment.severity,
            category="OTHER",
            latitude=assessment.latitude,
            longitude=assessment.longitude,
            geom=f"SRID=4326;POINT({assessment.longitude} {assessment.latitude})",
            risk_score=assessment.risk_score,
        )
        session.add(incident)
        await session.flush()
        return incident
