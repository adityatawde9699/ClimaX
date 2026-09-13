import os
from uuid import uuid4

import httpx
import pytest
from main import app
from security.jwt import hash_password

from core.database import AsyncSessionLocal
from models.entities import User

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DATABASE_TESTS") != "1",
    reason="requires PostgreSQL/PostGIS and migrated schema",
)


@pytest.mark.asyncio
async def test_auth_report_and_retrieval_flow():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"citizen-{uuid4()}@example.com"
        registration = await client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "full_name": "Integration Citizen",
                "password": "secure-password-123",
            },
        )
        assert registration.status_code == 201, registration.text
        token = registration.json()["access_token"]

        login = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": "secure-password-123"}
        )
        assert login.status_code == 200

        report = await client.post(
            "/api/v1/reports/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "location": {"latitude": 28.6139, "longitude": 77.209},
                "category": "WASTE_INCINERATION",
                "description": "Visible smoke from roadside waste",
                "media_urls": [],
            },
        )
        assert report.status_code == 200, report.text
        report_id = report.json()["data"]["id"]
        retrieved = await client.get(f"/api/v1/reports/{report_id}")
        assert retrieved.status_code == 200
        assert retrieved.json()["data"]["id"] == report_id


@pytest.mark.asyncio
async def test_authority_operational_flow():
    authority_id = str(uuid4())
    email = f"authority-{authority_id}@example.com"
    async with AsyncSessionLocal() as database:
        database.add(
            User(
                id=authority_id,
                email=email,
                full_name="Authority",
                password_hash=hash_password("secure-password-123"),
                role="AUTHORITY",
                organization_id="org-delhi-pollution-control-committee",
            )
        )
        await database.commit()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        login = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": "secure-password-123"}
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        nearby = await client.get("/api/v1/sensors/nearby?lat=28.65&lng=77.31&radius_m=5000")
        assert nearby.status_code == 200 and nearby.json()["total"] >= 1
        observation = await client.post(
            "/api/v1/environment/observations",
            headers=headers,
            json={
                "sensor_id": "sn-cpcb-anand-vihar-ref",
                "timestamp": "2026-09-13T12:00:00Z",
                "pm25": 85.0,
            },
        )
        assert observation.status_code == 200, observation.text
        incident = await client.post(
            "/api/v1/incidents/",
            headers=headers,
            json={
                "title": "Integration smoke",
                "severity": "HIGH",
                "category": "WASTE_INCINERATION",
                "location": {"latitude": 28.6, "longitude": 77.2},
            },
        )
        assert incident.status_code == 200, incident.text
        incident_id = incident.json()["data"]["id"]
        for target in ("INVESTIGATING", "DISPATCHED", "MITIGATED", "RESOLVED"):
            changed = await client.patch(
                f"/api/v1/incidents/{incident_id}/status", headers=headers, json={"status": target}
            )
            assert changed.status_code == 200, changed.text
        alert = await client.post(
            "/api/v1/alerts/",
            headers=headers,
            json={
                "title": "Air alert",
                "message": "Avoid exposure",
                "severity": "HIGH",
                "channel": "IN_APP",
            },
        )
        assert alert.status_code == 200, alert.text
        intervention = await client.post(
            "/api/v1/interventions/",
            headers=headers,
            json={
                "incident_id": incident_id,
                "intervention_type": "INSPECTION",
                "executing_agency": "DPCC",
                "action_summary": "Field inspection",
            },
        )
        assert intervention.status_code == 200, intervention.text
        intervention_id = intervention.json()["data"]["id"]
        completed = await client.patch(
            f"/api/v1/interventions/{intervention_id}/status",
            headers=headers,
            json={"status": "COMPLETED"},
        )
        assert completed.status_code == 200, completed.text
        analytics = await client.get("/api/v1/analytics/summary")
        assert analytics.status_code == 200 and analytics.json()["data"]["incidents"] >= 1
        assert (
            await client.get("/api/v1/environment/observations?sensor_id=sn-cpcb-anand-vihar-ref")
        ).status_code == 200
        assert (
            await client.get("/api/v1/reports/?status=SUBMITTED&bbox=77,28,78,29")
        ).status_code == 200
        assert (await client.get(f"/api/v1/incidents/{incident_id}")).status_code == 200
        assert (await client.get("/api/v1/alerts/?severity=HIGH&active=true")).status_code == 200


@pytest.mark.asyncio
async def test_admin_user_crud_flow():
    admin_id = str(uuid4())
    email = f"admin-{admin_id}@example.com"
    async with AsyncSessionLocal() as database:
        database.add(
            User(
                id=admin_id,
                email=email,
                full_name="Admin",
                password_hash=hash_password("secure-password-123"),
                role="ADMIN",
            )
        )
        await database.commit()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        login = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": "secure-password-123"}
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        created = await client.post(
            "/api/v1/users/",
            headers=headers,
            json={
                "email": f"researcher-{uuid4()}@example.com",
                "full_name": "Researcher",
                "password": "secure-password-123",
                "role": "RESEARCHER",
            },
        )
        assert created.status_code == 201, created.text
        user_id = created.json()["data"]["id"]
        assert (await client.get(f"/api/v1/users/{user_id}", headers=headers)).status_code == 200
        updated = await client.patch(
            f"/api/v1/users/{user_id}", headers=headers, json={"preferred_language": "hi"}
        )
        assert updated.status_code == 200 and updated.json()["data"]["preferred_language"] == "hi"
