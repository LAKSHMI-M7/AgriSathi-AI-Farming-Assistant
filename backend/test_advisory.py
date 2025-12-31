import httpx
import asyncio

async def test_advisory():
    base_url = "http://127.0.0.1:8001/weather/current"
    params = {
        "lat": 10.8505,
        "lon": 76.2711,
        "lang": "ml"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(base_url, params=params)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print("Summary:", data.get('summary'))
                print("Advisory Keys:", data.get('advisory').keys())
                print("Labels:", data.get('labels'))
            else:
                print("Error:", resp.text)
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    # Ensure uvicorn is running on 8001
    asyncio.run(test_advisory())
