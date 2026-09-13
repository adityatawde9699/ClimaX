"""Async PostgreSQL session management for the ClimaX API."""

import asyncio
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    connect_args={
        "timeout": settings.DB_TIMEOUT_SECONDS,
        "command_timeout": settings.DB_TIMEOUT_SECONDS,
    },
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield one transactional session for a request and close it afterwards."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def database_is_healthy() -> bool:
    """Return whether the configured database accepts a minimal query."""

    async def ping() -> None:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

    try:
        await asyncio.wait_for(ping(), timeout=settings.DB_TIMEOUT_SECONDS)
        return True
    except Exception:
        return False
