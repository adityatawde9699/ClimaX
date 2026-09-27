import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from api.v1.auth import login
from core.config import Settings
from core.config import settings as current_settings
from schemas.auth import LoginRequest


def test_production_rejects_development_defaults():
    with pytest.raises(ValidationError, match="Invalid production configuration"):
        Settings(ENVIRONMENT="production", _env_file=None)


def test_production_accepts_explicit_secure_configuration():
    settings = Settings(
        ENVIRONMENT="production",
        DEBUG=False,
        ENABLE_API_DOCS=False,
        JWT_SECRET_KEY="production-test-key-that-is-longer-than-32-bytes",
        DATABASE_URL="postgresql+asyncpg://service:secret@db:5432/climax",
        DATABASE_SYNC_URL="postgresql+psycopg2://service:secret@db:5432/climax",
        CORS_ORIGINS=["https://climax.example.com"],
        _env_file=None,
    )

    assert settings.ENVIRONMENT == "production"


def test_production_rejects_demo_login():
    with pytest.raises(ValidationError, match="ENABLE_DEMO_LOGIN must be false"):
        Settings(
            ENVIRONMENT="production",
            DEBUG=False,
            ENABLE_API_DOCS=False,
            ENABLE_DEMO_LOGIN=True,
            JWT_SECRET_KEY="production-test-key-that-is-longer-than-32-bytes",
            DATABASE_URL="postgresql+asyncpg://service:secret@db:5432/climax",
            DATABASE_SYNC_URL="postgresql+psycopg2://service:secret@db:5432/climax",
            CORS_ORIGINS=["https://climax.example.com"],
            _env_file=None,
        )


def test_public_demo_requires_secure_configuration():
    with pytest.raises(ValidationError, match="Invalid production configuration"):
        Settings(ENVIRONMENT="demo", ENABLE_DEMO_LOGIN=True, _env_file=None)


def test_public_demo_accepts_explicit_secure_configuration():
    settings = Settings(
        ENVIRONMENT="demo",
        DEBUG=False,
        ENABLE_API_DOCS=False,
        ENABLE_DEMO_LOGIN=True,
        JWT_SECRET_KEY="demo-test-key-that-is-longer-than-32-bytes",
        DATABASE_URL="postgresql+asyncpg://service:secret@db:5432/climax_demo",
        DATABASE_SYNC_URL="postgresql+psycopg2://service:secret@db:5432/climax_demo",
        CORS_ORIGINS=["https://climaxevs.vercel.app"],
        _env_file=None,
    )
    assert settings.ENVIRONMENT == "demo"


@pytest.mark.asyncio
async def test_production_rejects_demo_password_login(monkeypatch):
    monkeypatch.setattr(current_settings, "ENVIRONMENT", "production")
    with pytest.raises(HTTPException) as error:
        await login(LoginRequest(email="demo@climax.local", password="irrelevant"), db=None)
    assert error.value.status_code == 401
