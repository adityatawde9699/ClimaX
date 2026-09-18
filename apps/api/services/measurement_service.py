from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import select

from models.entities import EnvironmentalObservation, Intervention, InterventionMeasurement


class MeasurementService:
    async def record_from_observations(
        self, session, intervention: Intervention
    ) -> InterventionMeasurement | None:
        pre_pm25 = await session.scalar(
            select(EnvironmentalObservation.pm25)
            .where(
                EnvironmentalObservation.pm25.is_not(None),
                EnvironmentalObservation.timestamp <= intervention.dispatched_at,
            )
            .order_by(EnvironmentalObservation.timestamp.desc())
            .limit(1)
        )
        post_pm25 = await session.scalar(
            select(EnvironmentalObservation.pm25)
            .where(
                EnvironmentalObservation.pm25.is_not(None),
                EnvironmentalObservation.timestamp > intervention.dispatched_at,
            )
            .order_by(EnvironmentalObservation.timestamp.asc())
            .limit(1)
        )
        if pre_pm25 is None or post_pm25 is None:
            return None
        return await self.record(session, intervention.id, pre_pm25, post_pm25)

    async def record(
        self,
        session,
        intervention_id: str,
        pre_pm25: float,
        post_pm25: float,
        window_hours: int = 6,
    ) -> InterventionMeasurement:
        delta = ((post_pm25 - pre_pm25) / pre_pm25 * 100) if pre_pm25 else 0.0
        item = InterventionMeasurement(
            id=str(uuid4()),
            intervention_id=intervention_id,
            pre_intervention_pm25=pre_pm25,
            post_intervention_pm25=post_pm25,
            delta_pm25_percent=delta,
            evaluation_window_hours=window_hours,
            is_statistically_significant=abs(delta) >= 10,
            measured_at=datetime.now(UTC),
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item
