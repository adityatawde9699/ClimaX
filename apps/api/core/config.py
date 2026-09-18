"""
ClimaX Core Configuration Module
Loads and validates environment configurations using Pydantic Settings.
"""

from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "ClimaX Platform API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    ENABLE_API_DOCS: bool = True
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database
    DATABASE_URL: str = (
        "postgresql+asyncpg://climax_user:climax_dev_password@localhost:5432/climax_db"
    )
    DATABASE_SYNC_URL: str = (
        "postgresql+psycopg2://climax_user:climax_dev_password@localhost:5432/climax_db"
    )
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_TIMEOUT_SECONDS: int = 3

    # Google Cloud & AI
    GCP_PROJECT_ID: str = "climax-prod-project-id"
    GCP_REGION: str = "us-central1"
    GOOGLE_OAUTH_CLIENT_ID: str = ""
    PUBSUB_EMULATOR_HOST: str = ""
    GCS_BUCKET: str = "climax-development"
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    REDIS_URL: str = "redis://localhost:6379/0"
    PREDICTION_CACHE_TTL_SECONDS: int = 3600
    RISK_CACHE_TTL_SECONDS: int = 900
    PUBSUB_SENSOR_SUBSCRIPTION: str = "climax-sensor-ingest-sub"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_TEXT: str = "gemini-1.5-pro"
    GEMINI_MODEL_MULTIMODAL: str = "gemini-1.5-pro"

    # Vertex AI
    VERTEX_AI_ENDPOINT_POLLUTION_PREDICTION: str = ""

    # Auth & Security
    JWT_SECRET_KEY: str = "development-secret-key-change-in-production-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AUTHORITY_REGISTRATION_CODE: str = ""
    RISK_AUTO_INCIDENT_ORGANIZATION_ID: str = ""
    MAX_REPORT_UPLOAD_BYTES: int = 10_000_000

    @model_validator(mode="after")
    def validate_production_configuration(self):
        if self.ENVIRONMENT.lower() != "production":
            return self
        problems = []
        if self.DEBUG:
            problems.append("DEBUG must be false")
        if self.ENABLE_API_DOCS:
            problems.append("ENABLE_API_DOCS must be false")
        if (
            self.JWT_SECRET_KEY == "development-secret-key-change-in-production-32-chars"
            or len(self.JWT_SECRET_KEY) < 32
        ):
            problems.append("JWT_SECRET_KEY must be replaced with at least 32 characters")
        if "climax_dev_password" in self.DATABASE_URL or "climax_dev_password" in self.DATABASE_SYNC_URL:
            problems.append("development database credentials must be replaced")
        if any("localhost" in origin or "127.0.0.1" in origin for origin in self.CORS_ORIGINS):
            problems.append("CORS_ORIGINS must contain only deployed origins")
        if problems:
            raise ValueError("Invalid production configuration: " + "; ".join(problems))
        return self

    model_config = SettingsConfigDict(
        env_file=ROOT_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
