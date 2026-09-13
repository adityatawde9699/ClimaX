"""
ClimaX FastAPI Application Entrypoint
Establishes the API lifecycle, CORS policies, global exception filters, and mounts versioned routers.
Phase 2 Core API Foundation.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
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


@app.get("/health", tags=["Health"])
async def health_check():
    """System health check endpoint, including database connectivity."""
    database_healthy = await database_is_healthy()
    return {
        "status": "healthy" if database_healthy else "degraded",
        "database": "healthy" if database_healthy else "unavailable",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Mount versioned API router
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
