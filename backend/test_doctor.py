
import httpx
import asyncio

async def test_doctor():
    url = "http://localhost:8000/doctor/analyze"
    files = {'file': ('test.jpg', b'fake content', 'image/jpeg')}
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, files=files)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_doctor())
