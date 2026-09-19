from unittest.mock import AsyncMock

import httpx
import jwt
import pytest
from events.broker import broker
from main import app

from core.config import settings


class FakeSocket:
    def __init__(self):
        self.accept = AsyncMock()
        self.send_json = AsyncMock()


@pytest.mark.asyncio
async def test_authenticated_realtime_probe_reaches_connected_client():
    token = jwt.encode(
        {"sub": "realtime-test", "role": "ADMIN"},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    socket = FakeSocket()
    await broker.connect(socket)
    try:
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/health/realtime-probe",
                headers={"Authorization": f"Bearer {token}"},
            )
        assert response.status_code == 200
        socket.send_json.assert_awaited_once_with(
            {
                "event": "system.realtime_probe",
                "data": {"id": response.json()["probe_id"]},
            }
        )
    finally:
        broker.disconnect(socket)


@pytest.mark.asyncio
async def test_realtime_probe_requires_authentication():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/health/realtime-probe")
    assert response.status_code == 401
