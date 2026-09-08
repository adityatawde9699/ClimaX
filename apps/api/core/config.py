"""
ClimaX Core Configuration Module
Loads and validates environment configurations using Pydantic Settings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "ClimaX Platform API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://climax_user:climax_dev_password@localhost:5432/climax_db"
    DATABASE_SYNC_URL: str = "postgresql+psycopg2://climax_user:climax_dev_password@localhost:5432/climax_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Google Cloud & AI
    GCP_PROJECT_ID: str = "climax-prod-project-id"
    GCP_REGION: str = "us-central1"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_TEXT: str = "gemini-1.5-pro"
    GEMINI_MODEL_MULTIMODAL: str = "gemini-1.5-pro"
    
    # Vertex AI
    VERTEX_AI_ENDPOINT_POLLUTION_PREDICTION: str = ""

    # Auth & Security
    JWT_SECRET_KEY: str = "development-secret-key-change-in-production-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
