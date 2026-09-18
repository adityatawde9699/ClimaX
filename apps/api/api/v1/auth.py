import asyncio
import secrets
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from pydantic import BaseModel
from security.jwt import create_access_token, hash_password, verify_password
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import get_db
from models.entities import User
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


class GoogleLoginRequest(BaseModel):
    credential: str


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    if payload.role.value == "ADMIN":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Administrator accounts must be provisioned by an existing administrator",
        )
    if payload.role.value == "AUTHORITY" and (
        not settings.AUTHORITY_REGISTRATION_CODE
        or not payload.authority_registration_code
        or not secrets.compare_digest(
            payload.authority_registration_code, settings.AUTHORITY_REGISTRATION_CODE
        )
    ):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "A valid authority registration code is required",
        )
    if await db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered")
    user = User(
        id=str(uuid4()),
        email=str(payload.email),
        full_name=payload.full_name,
        role=payload.role.value,
        organization_id=None,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return TokenResponse(access_token=create_access_token(user))


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == payload.email))
    if user is None or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    return TokenResponse(access_token=create_access_token(user))


@router.post("/google", response_model=TokenResponse)
async def google_login(payload: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    """Verify a Google Identity Services ID token and issue a ClimaX JWT."""
    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Google login is not configured")
    try:
        claims = await asyncio.to_thread(
            google_id_token.verify_oauth2_token,
            payload.credential,
            google_requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Google identity token") from exc
    email = claims.get("email")
    if not email or not claims.get("email_verified"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Google email is not verified")
    google_sub = claims.get("sub")
    if not google_sub:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Google account identifier is missing")
    user = await db.scalar(select(User).where(User.google_sub == google_sub))
    if user is None:
        user = await db.scalar(select(User).where(User.email == email))
    if user is not None and user.google_sub not in (None, google_sub):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email is linked to another Google account")
    if user is None:
        user = User(
            id=str(uuid4()),
            email=email,
            full_name=claims.get("name") or email.split("@", 1)[0],
            role="CITIZEN",
            organization_id=None,
            password_hash=None,
            google_sub=google_sub,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    elif user.google_sub is None:
        user.google_sub = google_sub
        await db.commit()
        await db.refresh(user)
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User account is inactive")
    return TokenResponse(access_token=create_access_token(user))
