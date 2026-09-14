"""
ClimaX API v1 Unified Router Aggregator
Mounts all domain module boundaries under the /api/v1 prefix.
"""

from fastapi import APIRouter

from api.v1.ai import router as ai_router
from api.v1.alerts import router as alerts_router
from api.v1.analytics import router as analytics_router
from api.v1.auth import router as auth_router
from api.v1.environment import router as environment_router
from api.v1.incidents import router as incidents_router
from api.v1.interventions import router as interventions_router
from api.v1.predictions import router as predictions_router
from api.v1.reports import router as reports_router
from api.v1.risk import router as risk_router
from api.v1.sensors import router as sensors_router
from api.v1.users import router as users_router
from api.v1.weather import router as weather_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router)

api_v1_router.include_router(users_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(environment_router)
api_v1_router.include_router(sensors_router)
api_v1_router.include_router(incidents_router)
api_v1_router.include_router(predictions_router)
api_v1_router.include_router(risk_router)
api_v1_router.include_router(alerts_router)
api_v1_router.include_router(interventions_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(ai_router)
api_v1_router.include_router(weather_router)
