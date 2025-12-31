import asyncio
import httpx
from app.services.weather_service import get_weather_advisory
from app.core.config import settings

async def main():
    print(f"Testing with API Key: {settings.OPENWEATHER_API_KEY[:5]}...")
    data = await get_weather_advisory(10.8505, 76.2711)
    if "error" in data:
        print(f"Error: {data['error']}")
    else:
        print(f"Location: {data['location']}")
        print(f"Temp: {data['temp']}")
        print(f"Forecast count: {len(data['forecast'])}")
        print(f"Advisory: {list(data['advisory'].keys())}")

if __name__ == "__main__":
    asyncio.run(main())
