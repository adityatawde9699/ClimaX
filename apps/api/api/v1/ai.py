"""
AI API Router — /api/v1/ai
Boundary for Gemini Multimodal report classification, AI Copilot reasoning, and source attribution.
Implementation scheduled for Phase 5 and Phase 10.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from schemas.entities import AIAnalysisRead
from schemas.base import ApiResponse

router = APIRouter(prefix="/ai", tags=["AI Orchestration"])


class MultimodalInferenceRequest(BaseModel):
    media_url: str
    latitude: float
    longitude: float
    user_notes: str


class CopilotQueryRequest(BaseModel):
    session_id: str
    query: str


@router.post("/analyze-report", response_model=ApiResponse[AIAnalysisRead], summary="Perform multimodal pollution analysis on report")
async def analyze_report_multimodal(payload: MultimodalInferenceRequest):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Gemini multimodal integration begins in Phase 5."
    )


@router.post("/copilot", response_model=ApiResponse[dict], summary="Query environmental AI copilot")
async def query_copilot(query: CopilotQueryRequest):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. Copilot reasoning implementation begins in Phase 10."
    )
