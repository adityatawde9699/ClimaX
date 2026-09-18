import pytest
from fastapi import HTTPException

from api.v1.auth import register
from schemas.auth import RegisterRequest
from schemas.entities import UserRole


def test_registration_accepts_supported_workspace_roles():
    payload = RegisterRequest(
        email="researcher@example.com",
        full_name="Climate Researcher",
        password="long-enough-password",
        role=UserRole.RESEARCHER,
    )

    assert payload.role is UserRole.RESEARCHER


@pytest.mark.asyncio
async def test_public_registration_rejects_admin_role():
    payload = RegisterRequest(
        email="admin@example.com",
        full_name="Admin Attempt",
        password="long-enough-password",
        role=UserRole.ADMIN,
    )

    with pytest.raises(HTTPException) as raised:
        await register(payload, None)  # type: ignore[arg-type]

    assert raised.value.status_code == 403


@pytest.mark.asyncio
async def test_authority_registration_requires_server_code():
    payload = RegisterRequest(
        email="authority@example.com",
        full_name="Authority Attempt",
        password="long-enough-password",
        role=UserRole.AUTHORITY,
    )

    with pytest.raises(HTTPException) as raised:
        await register(payload, None)  # type: ignore[arg-type]

    assert raised.value.status_code == 403
