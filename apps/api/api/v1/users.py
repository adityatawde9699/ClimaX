"""Database-backed user administration and profile routes."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from security.jwt import get_current_user, hash_password, require_roles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.entities import User
from schemas.base import ApiResponse
from schemas.entities import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=ApiResponse[UserRead], status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles("ADMIN")),
):
    if await db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered")
    values = payload.model_dump(exclude={"password"})
    values["role"] = payload.role.value
    user = User(id=str(uuid4()), password_hash=hash_password(payload.password), **values)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return ApiResponse(data=user)


@router.get("/me", response_model=ApiResponse[UserRead])
async def get_current_user_profile(user: User = Depends(get_current_user)):
    return ApiResponse(data=user)


@router.get("/{user_id}", response_model=ApiResponse[UserRead])
async def get_user(
    user_id: str, db: AsyncSession = Depends(get_db), current: User = Depends(get_current_user)
):
    if current.id != user_id and current.role != "ADMIN":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot read another user")
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return ApiResponse(data=user)


@router.patch("/{user_id}", response_model=ApiResponse[UserRead])
async def update_user(
    user_id: str,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    if current.id != user_id and current.role != "ADMIN":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot update another user")
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    changes = payload.model_dump(exclude_unset=True)
    if current.role != "ADMIN" and {"role", "organization_id", "is_active"}.intersection(changes):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only admins may change privileged fields")
    if "role" in changes:
        changes["role"] = changes["role"].value
    for field, value in changes.items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return ApiResponse(data=user)
