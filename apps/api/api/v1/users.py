"""
Users API Router — /api/v1/users
Boundary for authentication profiles, authority accounts, and citizen accounts.
Implementation scheduled for Phase 2.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from schemas.entities import UserRead
from schemas.base import ApiResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=ApiResponse[UserRead], summary="Get current user profile")
async def get_current_user_profile():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Phase 0: Architecture scaffolding only. User auth implementation begins in Phase 2."
    )
