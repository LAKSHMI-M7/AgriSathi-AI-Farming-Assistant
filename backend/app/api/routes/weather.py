from fastapi import APIRouter, Query
from app.services.weather_service import get_weather_advisory, search_weather_advisory

router = APIRouter()

@router.get("/current")
async def get_weather(
    lat: float = 10.8505, 
    lon: float = 76.2711, 
    lang: str = Query("en", description="Language code: en, ml, or ta")
):
    """Returns detailed farmer-focused weather advisory for coordinates."""
    return await get_weather_advisory(lat, lon, lang)

@router.get("/search")
async def search_weather(
    query: str = Query(..., description="District or State name"),
    lang: str = Query("en", description="Language code")
):
    """Returns detailed farmer-focused weather advisory for a named location."""
    return await search_weather_advisory(query, lang)
