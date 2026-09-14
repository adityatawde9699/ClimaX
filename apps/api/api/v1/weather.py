import httpx
from fastapi import APIRouter, HTTPException, Query
from integrations.weather_adapter import WeatherAdapter

from schemas.base import ApiResponse

router = APIRouter(prefix="/weather", tags=["Weather"])
weather = WeatherAdapter()


@router.get("", response_model=ApiResponse[dict[str, float | None]])
async def get_weather(
    lat: float = Query(..., ge=-90, le=90), lng: float = Query(..., ge=-180, le=180)
):
    try:
        return ApiResponse(data=await weather.get_current_meteorology(lat, lng))
    except httpx.HTTPError as exc:
        raise HTTPException(503, "Weather provider unavailable") from exc
