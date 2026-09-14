from datetime import UTC, datetime
from uuid import uuid4

from models.entities import InterventionMeasurement


class MeasurementService:
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
