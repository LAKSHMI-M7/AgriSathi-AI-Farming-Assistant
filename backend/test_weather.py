
import httpx
import asyncio

async def check_weather():
    lat = 10.8505
    lon = 76.2711
    api_key = "75ed6b1d1d3d8b7a82dc9936f22ee2b3"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text}")

if __name__ == "__main__":
    asyncio.run(check_weather())
