import pytest
from pydantic import ValidationError

from core.config import Settings


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
