"""Seed a small, repeatable ClimaX demo dataset into the configured database."""

import asyncio
from datetime import UTC, datetime, timedelta

from integrations.cache import cache
from security.jwt import hash_password
from sqlalchemy import select

from core.config import settings
from core.database import AsyncSessionLocal
from models.entities import (
    AIAnalysis,
    Alert,
    CitizenReport,
    DataSource,
    EnvironmentalObservation,
    Incident,
    Intervention,
    Organization,
    Prediction,
    RiskAssessment,
    Sensor,
    User,
)

DEMO_ORG_ID = "demo-org-delhi"
DEMO_SOURCE_ID = "demo-source-cpcb"
DEMO_AUTHORITY_ID = "demo-authority-user"
DEMO_CITIZEN_ID = "demo-citizen-user"
DEMO_RESEARCHER_ID = "demo-researcher-user"


async def existing(session, model, item_id: str):
    return await session.get(model, item_id)


async def seed() -> None:
    if settings.ENVIRONMENT.lower() not in {"development", "demo"}:
        raise RuntimeError("Demo records can only be seeded in development or demo")
    now = datetime.now(UTC)
    async with AsyncSessionLocal() as session:
        organization = await existing(session, Organization, DEMO_ORG_ID)
        if organization is None:
            organization = Organization(
                id=DEMO_ORG_ID,
                name="ClimaX Delhi Environmental Operations",
                jurisdiction_code="DL-DEMO",
                department="Air Quality Response Cell",
                contact_email="operations@climax.demo",
            )
            session.add(organization)

        source = await existing(session, DataSource, DEMO_SOURCE_ID)
        if source is None:
            source = DataSource(
                id=DEMO_SOURCE_ID,
                name="Demo civic sensor network",
                source_type="SENSOR_NETWORK",
                provider="ClimaX demo feed",
                refresh_interval_seconds=300,
                meta_info={"demo": True, "coverage": "Delhi NCR"},
            )
            session.add(source)

        demo_accounts = (
            (
                DEMO_CITIZEN_ID,
                "demo@climax.local",
                "ClimaX Demo Citizen",
                "CITIZEN",
                "ClimaXDemo2026!",
                None,
            ),
            (
                DEMO_AUTHORITY_ID,
                "authority@climax.local",
                "ClimaX Demo Authority",
                "AUTHORITY",
                "ClimaXAuthority2026!",
                DEMO_ORG_ID,
            ),
            (
                DEMO_RESEARCHER_ID,
                "researcher@climax.local",
                "ClimaX Demo Researcher",
                "RESEARCHER",
                "ClimaXResearcher2026!",
                None,
            ),
        )
        account_ids = {}
        for user_id, email, name, role, password, organization_id in demo_accounts:
            user = await session.scalar(select(User).where(User.email == email))
            if user is None:
                user = User(
                    id=user_id,
                    email=email,
                    full_name=name,
                    password_hash=hash_password(password),
                    role=role,
                    organization_id=organization_id,
                    preferred_language="en",
                    is_active=True,
                )
                session.add(user)
            elif user.role != role:
                raise RuntimeError(f"Existing demo email {email} has the wrong role")
            account_ids[role] = user.id

        sensors = [
            ("demo-sensor-01", "CXM-DEL-001", "Connaught Place", 28.6315, 77.2167, 168),
            ("demo-sensor-02", "CXM-DEL-002", "Anand Vihar", 28.6469, 77.3150, 242),
            ("demo-sensor-03", "CXM-DEL-003", "Dwarka Sector 10", 28.5823, 77.0580, 92),
            ("demo-sensor-04", "CXM-DEL-004", "Lodhi Road", 28.5918, 77.2273, 118),
            ("demo-sensor-05", "CXM-DEL-005", "Rohini Sector 16", 28.7363, 77.1169, 146),
            ("demo-sensor-06", "CXM-DEL-006", "Noida Sector 62", 28.6270, 77.3649, 188),
        ]
        for sensor_id, external_id, _, latitude, longitude, aqi in sensors:
            sensor = await existing(session, Sensor, sensor_id)
            if sensor is None:
                sensor = Sensor(
                    id=sensor_id,
                    data_source_id=DEMO_SOURCE_ID,
                    external_sensor_id=external_id,
                    sensor_type="GOVERNMENT_STATION",
                    model_name="ClimaX AirNode v2",
                    latitude=latitude,
                    longitude=longitude,
                    geom=f"SRID=4326;POINT({longitude} {latitude})",
                    is_calibrated=True,
                    is_active=True,
                    last_ping_at=now - timedelta(minutes=2),
                )
                session.add(sensor)
            else:
                sensor.last_ping_at = now - timedelta(minutes=2)
            observation_id = f"demo-observation-{sensor_id[-2:]}"
            observation = await existing(session, EnvironmentalObservation, observation_id)
            if observation is None:
                pm25 = round(aqi / 4.2, 1)
                session.add(
                    EnvironmentalObservation(
                        id=observation_id,
                        sensor_id=sensor_id,
                        timestamp=now - timedelta(minutes=8),
                        tier="OBSERVED",
                        quality_flag="VALID",
                        pm25=pm25,
                        pm10=round(pm25 * 1.65, 1),
                        no2=round(18 + aqi / 18, 1),
                        so2=5.4,
                        co=0.8,
                        o3=32.0,
                        aqi=aqi,
                        temperature_c=27.4,
                        humidity_percent=48.0,
                        wind_speed_kmh=8.6,
                        wind_direction_deg=285.0,
                    )
                )
            else:
                observation.timestamp = now - timedelta(minutes=8)

            for horizon, forecast_aqi in ((6, aqi + 8), (24, aqi + 22), (72, aqi - 12)):
                prediction_id = f"demo-prediction-{sensor_id[-2:]}-{horizon}"
                prediction = await existing(session, Prediction, prediction_id)
                if prediction is None:
                    predicted_pm25 = round(forecast_aqi / 4.2, 1)
                    session.add(
                        Prediction(
                            id=prediction_id,
                            sensor_id=sensor_id,
                            latitude=latitude,
                            longitude=longitude,
                            forecast_timestamp=now + timedelta(hours=horizon),
                            horizon_hours=horizon,
                            tier="PREDICTED",
                            predicted_pm25=predicted_pm25,
                            predicted_aqi=forecast_aqi,
                            confidence_interval_low=max(0, forecast_aqi - 18),
                            confidence_interval_high=forecast_aqi + 18,
                            explanation={
                                "summary": "Demo forecast based on recent sensor trend and wind conditions.",
                                "drivers": [
                                    "PM2.5 trend",
                                    "wind direction",
                                    "neighbourhood baseline",
                                ],
                                "demo": True,
                            },
                        )
                    )
                else:
                    prediction.forecast_timestamp = now + timedelta(hours=horizon)

        risks = [
            ("demo-risk-01", 28.6469, 77.3150, 0.91, "CRITICAL", 0.84, 18, "PM2.5"),
            ("demo-risk-02", 28.6315, 77.2167, 0.73, "VERY_HIGH", 0.67, 11, "PM2.5"),
            ("demo-risk-03", 28.6270, 77.3649, 0.66, "HIGH", 0.59, 9, "NO2"),
            ("demo-risk-04", 28.5823, 77.0580, 0.28, "MODERATE", 0.31, 5, "PM10"),
        ]
        for (
            risk_id,
            latitude,
            longitude,
            score,
            severity,
            vulnerability,
            receptors,
            pollutant,
        ) in risks:
            risk = await existing(session, RiskAssessment, risk_id)
            if risk is None:
                session.add(
                    RiskAssessment(
                        id=risk_id,
                        latitude=latitude,
                        longitude=longitude,
                        risk_score=score,
                        severity=severity,
                        population_vulnerability_index=vulnerability,
                        sensitive_receptors_count=receptors,
                        dominant_pollutant=pollutant,
                        calculated_at=now - timedelta(minutes=12),
                    )
                )
            else:
                risk.calculated_at = now - timedelta(minutes=12)

        alerts = [
            (
                "demo-alert-01",
                "Very high air pollution near Anand Vihar",
                "PM2.5 levels are elevated. Sensitive groups should reduce prolonged outdoor exposure.",
                "VERY_HIGH",
                4_000.0,
            ),
            (
                "demo-alert-02",
                "Traffic-related pollution detected in central Delhi",
                "Air quality is unhealthy for sensitive groups around Connaught Place.",
                "HIGH",
                2_500.0,
            ),
            (
                "demo-alert-03",
                "Demo network online",
                "Six civic sensors are reporting successfully.",
                "LOW",
                None,
            ),
        ]
        for alert_id, title, message, severity, radius in alerts:
            alert = await existing(session, Alert, alert_id)
            if alert is None:
                session.add(
                    Alert(
                        id=alert_id,
                        title=title,
                        message=message,
                        severity=severity,
                        channel="IN_APP",
                        affected_radius_m=radius,
                        is_dispatched=True,
                        dispatched_at=now - timedelta(minutes=20),
                        expires_at=now + timedelta(days=1),
                    )
                )
            else:
                alert.expires_at = now + timedelta(days=1)

        incidents = [
            (
                "demo-incident-01",
                "Anand Vihar particulate matter spike",
                "CRITICAL",
                "INDUSTRIAL_EMISSION",
                28.6469,
                77.3150,
                "DISPATCHED",
                0.91,
            ),
            (
                "demo-incident-02",
                "Central Delhi traffic corridor exceedance",
                "VERY_HIGH",
                "VEHICULAR_CONGESTION",
                28.6315,
                77.2167,
                "INVESTIGATING",
                0.73,
            ),
            (
                "demo-incident-03",
                "Noida construction dust report",
                "HIGH",
                "CONSTRUCTION_DUST",
                28.6270,
                77.3649,
                "OPEN",
                0.66,
            ),
        ]
        for (
            incident_id,
            title,
            severity,
            category,
            latitude,
            longitude,
            status,
            risk_score,
        ) in incidents:
            incident = await existing(session, Incident, incident_id)
            if incident is None:
                session.add(
                    Incident(
                        id=incident_id,
                        organization_id=DEMO_ORG_ID,
                        title=title,
                        status=status,
                        severity=severity,
                        category=category,
                        latitude=latitude,
                        longitude=longitude,
                        geom=f"SRID=4326;POINT({longitude} {latitude})",
                        assigned_officer_id=account_ids["AUTHORITY"],
                        risk_score=risk_score,
                        root_cause_summary="Demo incident seeded for dashboard walkthrough.",
                    )
                )
            else:
                incident.category = category

        interventions = [
            (
                "demo-intervention-01",
                "demo-incident-01",
                "ROAD_WATERING",
                "Delhi Pollution Control Committee",
                "Dispatched water tanker and field team to suppress resuspended dust.",
                True,
            ),
            (
                "demo-intervention-02",
                "demo-incident-02",
                "TRAFFIC_DIVERSION",
                "Delhi Traffic Police",
                "Traffic management team deployed during the evening peak window.",
                False,
            ),
        ]
        for (
            intervention_id,
            incident_id,
            intervention_type,
            agency,
            summary,
            completed,
        ) in interventions:
            if await existing(session, Intervention, intervention_id) is None:
                dispatched_at = now - timedelta(hours=3)
                session.add(
                    Intervention(
                        id=intervention_id,
                        incident_id=incident_id,
                        intervention_type=intervention_type,
                        dispatched_at=dispatched_at,
                        executed_at=dispatched_at + timedelta(minutes=25),
                        completed_at=dispatched_at + timedelta(hours=2) if completed else None,
                        executing_agency=agency,
                        action_summary=summary,
                    )
                )

        report_id = "demo-report-01"
        if await existing(session, CitizenReport, report_id) is None:
            session.add(
                CitizenReport(
                    id=report_id,
                    user_id=account_ids["CITIZEN"],
                    tier="OBSERVED",
                    latitude=28.6462,
                    longitude=77.3145,
                    geom="SRID=4326;POINT(77.3145 28.6462)",
                    address_text="Anand Vihar, Delhi",
                    category="OTHER",
                    description="Visible haze and strong exhaust odour reported during the morning commute.",
                    media_urls=[],
                    status="UNDER_REVIEW",
                    incident_id="demo-incident-01",
                )
            )
        else:
            report = await existing(session, CitizenReport, report_id)
            report.user_id = account_ids["CITIZEN"]

        analysis_id = "demo-analysis-01"
        if await existing(session, AIAnalysis, analysis_id) is None:
            session.add(
                AIAnalysis(
                    id=analysis_id,
                    report_id=report_id,
                    tier="INFERRED",
                    classification="OTHER",
                    explanation={
                        "result": "Reported haze is consistent with a particulate pollution event.",
                        "confidence": 0.87,
                        "confidence_tier": "HIGH",
                        "evidence": ["citizen report", "nearby sensor PM2.5", "wind direction"],
                        "data_sources": ["demo-report-01", "demo-sensor-02"],
                        "model": "ClimaX demo analysis",
                        "pollution_category": "OTHER",
                        "suggested_severity": "VERY_HIGH",
                    },
                    suggested_severity="VERY_HIGH",
                    confidence_score=0.87,
                    raw_model_response="Demo analysis record; no external inference call used.",
                )
            )

        await session.commit()

    await cache.delete_pattern("predictions:28.6:77.2:*")
    await cache.delete_pattern("risk:hotspots")
    print(
        "Seeded ClimaX demo data: 3 role accounts, 6 sensors, 6 observations, 18 predictions, 4 hotspots, 3 incidents, 2 interventions, 3 alerts, and 1 report."
    )


if __name__ == "__main__":
    asyncio.run(seed())
