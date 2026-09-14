"""Gemini analysis and role-aware copilot endpoints."""

from uuid import uuid4

from ai.copilot_service import AICopilotService
from ai.multimodal_analyzer import MultimodalReportAnalyzer
from fastapi import APIRouter, Depends, HTTPException
from integrations.gcs_adapter import GCSAdapter
from pydantic import BaseModel
from security.jwt import get_current_user
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import AIAnalysis, EnvironmentalObservation, Incident, User
from schemas.base import ApiResponse
from schemas.entities import AIAnalysisRead

router = APIRouter(prefix="/ai", tags=["AI Orchestration"])


class MultimodalInferenceRequest(BaseModel):
    media_url: str
    latitude: float
    longitude: float
    user_notes: str
    report_id: str | None = None


class CopilotQueryRequest(BaseModel):
    session_id: str
    query: str


def serialize_analysis(item: AIAnalysis) -> dict:
    return {
        "id": item.id,
        "report_id": item.report_id,
        "observation_id": item.observation_id,
        "tier": item.tier,
        "classification": item.classification,
        "explanation": item.explanation,
        "suggested_severity": item.suggested_severity,
        "confidence_score": item.confidence_score,
        "created_at": item.created_at,
    }


@router.post("/analyze-report", response_model=ApiResponse[AIAnalysisRead])
async def analyze_report_multimodal(
    payload: MultimodalInferenceRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    try:
        image = GCSAdapter().download_bytes(payload.media_url)
        analyzer = MultimodalReportAnalyzer()
        explanation = await analyzer.analyze(
            image, payload.latitude, payload.longitude, payload.user_notes
        )
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(503, str(exc)) from exc
    item = AIAnalysis(
        id=str(uuid4()),
        report_id=payload.report_id,
        tier="INFERRED",
        classification=explanation.pollution_category.value,
        explanation=explanation.model_dump(mode="json"),
        suggested_severity=explanation.suggested_severity,
        confidence_score=explanation.confidence,
        raw_model_response=analyzer.last_raw_response,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return ApiResponse(data=serialize_analysis(item))


@router.post("/copilot", response_model=ApiResponse[dict])
async def query_copilot(
    query: CopilotQueryRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    context = {
        "active_incidents": await db.scalar(
            select(func.count())
            .select_from(Incident)
            .where(Incident.status.not_in(["RESOLVED", "DISMISSED"]))
        )
        or 0,
        "observations": await db.scalar(select(func.count()).select_from(EnvironmentalObservation))
        or 0,
    }
    try:
        return ApiResponse(
            data=await AICopilotService().answer_query(
                query.session_id, user.role, query.query, context
            )
        )
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
