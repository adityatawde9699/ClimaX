"""
ClimaX Base API Envelopes & Query DTOs
"""

from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class CoordinatesDTO(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    altitude_m: Optional[float] = None
    accuracy_radius_m: Optional[float] = None


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[dict] = None


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: List[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 20
    total_pages: int = 1


class SpatialQueryFilter(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_km: Optional[float] = Field(default=5.0, ge=0.1, le=100.0)
