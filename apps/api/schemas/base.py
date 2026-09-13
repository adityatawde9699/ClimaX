"""
ClimaX Base API Envelopes & Query DTOs
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class CoordinatesDTO(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    altitude_m: float | None = None
    accuracy_radius_m: float | None = None


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    message: str | None = None
    error: dict | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 20
    total_pages: int = 1


class SpatialQueryFilter(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    radius_km: float | None = Field(default=5.0, ge=0.1, le=100.0)
