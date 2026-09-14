from uuid import uuid4

from models.entities import RiskAssessment


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
            calculated_at=__import__("datetime").datetime.now(__import__("datetime").UTC),
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item
