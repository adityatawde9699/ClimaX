"""
ClimaX FastAPI Application Entrypoint
Establishes the API lifecycle, CORS policies, global exception filters, and mounts versioned routers.
Phase 2 Core API Foundation.
"""

import asyncio
from contextlib import asynccontextmanager

import jwt
from events.broker import broker
from fastapi import FastAPI, Request, Response, WebSocket, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from observability.metrics import metrics_middleware, metrics_response
from sqlalchemy.exc import SQLAlchemyError

from api.v1.router import api_v1_router
from core.config import settings
from core.database import database_is_healthy
from core.exceptions import ClimaxBaseException
from core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ClimaX Platform API...")
    logger.info(f"Target Environment: {settings.ENVIRONMENT}")
    yield
    logger.info("Shutting down ClimaX Platform API...")


app = FastAPI(
    title="ClimaX — Federated AI Environmental Intelligence API",
    description=(
        "Production-grade backend API for ClimaX environmental monitoring, "
        "Gemini multimodal intelligence, Vertex AI plume prediction, and municipal action."
    ),
    version=settings.VERSION,
    docs_url="/docs" if settings.ENABLE_API_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if settings.ENABLE_API_DOCS else None,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(metrics_middleware)


@app.get("/metrics", include_in_schema=False)
async def metrics():
    return metrics_response()


@app.exception_handler(ClimaxBaseException)
async def climax_exception_handler(request: Request, exc: ClimaxBaseException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


@app.exception_handler(ConnectionRefusedError)
@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(
    request: Request, exc: SQLAlchemyError | ConnectionRefusedError
):
    """Return an actionable response when PostgreSQL/PostGIS is unavailable.

    Keeping database driver details out of the HTTP response avoids leaking the
    connection configuration and prevents expected local-infrastructure outages
    from appearing as an unhandled application error.
    """
    logger.warning(
        "Database request failed: path=%s exception_type=%s",
        request.url.path,
        exc.__class__.__name__,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled request failure: path=%s exception_type=%s",
        request.url.path,
        exc.__class__.__name__,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected server error occurred.",
                "details": None,
            },
        },
    )
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "success": False,
            "error": {
                "type": "DatabaseUnavailable",
                "message": (
                    "Database service is unavailable. Start PostgreSQL/PostGIS "
                    "and retry."
                ),
                "details": None,
            },
        },
    )


@app.get("/health", tags=["Health"])
async def health_check(response: Response):
    """System health check endpoint, including database connectivity."""
    database_healthy = await database_is_healthy()
    if not database_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {
        "status": "healthy" if database_healthy else "degraded",
        "database": "healthy" if database_healthy else "unavailable",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Mount versioned API router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.websocket("/ws/events")
async def events(socket: WebSocket):
    token = socket.query_params.get("token")
    try:
        jwt.decode(token or "", settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        await socket.close(code=1008)
        return
    await broker.connect(socket)
    try:
        while True:
            try:
                await asyncio.wait_for(socket.receive_text(), timeout=30)
            except TimeoutError:
                await socket.send_json({"event": "heartbeat"})
    except Exception:
        broker.disconnect(socket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
