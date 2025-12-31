
import httpx
import asyncio

async def test_news():
    async with httpx.AsyncClient() as client:
        # Test Default
        r1 = await client.get("http://localhost:8000/government/news")
        print("Default:", r1.status_code, len(r1.json()))
        
        # Test Kanchipuram
        r2 = await client.get("http://localhost:8000/government/news?location=Kanchipuram")
        print("Kanchipuram:", r2.status_code, r2.json()[0]['title'])

if __name__ == "__main__":
    asyncio.run(test_news())
