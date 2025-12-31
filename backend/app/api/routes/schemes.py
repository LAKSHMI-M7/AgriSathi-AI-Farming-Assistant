from fastapi import APIRouter, Query
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()

class Scheme(BaseModel):
    id: int
    name: str
    fullName: str
    description: str
    category: str
    crops: List[str]
    districts: List[str]
    eligibility: str
    amount: str
    status: str
    deadline: Optional[str] = None
    link: str
    ai_summary: str

SCHEMES_DATA = {
    "en": [
        {
            "id": 1,
            "name": "Subhiksha Keralam",
            "fullName": "Integrated Food Security Program for Kerala",
            "description": "Kerala's flagship program for food self-sufficiency through intensive cultivation and fallow land conversion.",
            "category": "subsidy",
            "crops": ["Paddy", "Vegetables", "Tuber crops"],
            "districts": ["Wayanad", "Palakkad", "Kozhikode", "Kannur"],
            "eligibility": "Small and marginal farmers residing in Kerala.",
            "amount": "Upto ₹50,000 / hectare",
            "status": "Active",
            "deadline": "2025-06-30",
            "link": "https://www.aims.kerala.gov.in/",
            "ai_summary": "🤖 AI SUMMARY: This scheme focuses on increasing food production by providing financial incentives to bring fallow land under cultivation. Highly recommended for young farmers."
        },
        {
            "id": 2,
            "name": "PM-Kisan Samman Nidhi",
            "fullName": "Pradhan Mantri Kisan Samman Nidhi",
            "description": "Income support scheme providing financial benefit to all landholding farmer families.",
            "category": "subsidy",
            "crops": ["All Crops"],
            "districts": ["All Districts"],
            "eligibility": "All landholding farmer families across India.",
            "amount": "₹6,000 / year",
            "status": "Active",
            "deadline": "No Deadline",
            "link": "https://pmkisan.gov.in/",
            "ai_summary": "🤖 AI SUMMARY: Direct benefit transfer of ₹2000 in three equal installments every four months. Essential for basic agricultural input costs."
        },
        {
            "id": 3,
            "name": "Mid-Day Meal Paddy Scheme",
            "fullName": "Paddy Procurement for School Meals",
            "description": "Special procurement drive for high-quality paddy for the school mid-day meal program.",
            "category": "equipment",
            "crops": ["Paddy"],
            "districts": ["Palakkad", "Alappuzha", "Kottayam"],
            "eligibility": "Registered paddy farmers with high-yield varieties.",
            "amount": "₹28.23 / kg",
            "status": "Seasonal",
            "deadline": "2025-03-15",
            "link": "https://supplycokerala.com/",
            "ai_summary": "🤖 AI SUMMARY: Ensures a guaranteed market price higher than the MSP for farmers participating in the school supply chain."
        },
        {
            "id": 4,
            "name": "Coconut Replanting Subsidy",
            "fullName": "Coconut Development Board Replanting Scheme",
            "description": "Financial assistance for removal of disease-affected palms and replanting with quality seedlings.",
            "category": "subsidy",
            "crops": ["Coconut"],
            "districts": ["Kozhikode", "Malappuram", "Wayanad", "Kanyakumari"],
            "eligibility": "Farmers with at least 0.1 hectare of coconut holding.",
            "amount": "₹15,000 / acre",
            "status": "Active",
            "deadline": "2025-12-31",
            "link": "https://www.coconutboard.gov.in/",
            "ai_summary": "🤖 AI SUMMARY: Aims to improve productivity by replacing old, unproductive palms with high-yielding varieties."
        }
    ],
    "ml": [
        {
            "id": 1,
            "name": "സുഭിക്ഷ കേരളം",
            "fullName": "കേരളത്തിനായുള്ള സംയോജിത ഭക്ഷ്യ സുരക്ഷാ പദ്ധതി",
            "description": "ഭക്ഷ്യ സ്വയംപര്യാപ്തത കൈവരിക്കുന്നതിനായുള്ള കേരള സർക്കാരിന്റെ ഏറ്റവും വലിയ പദ്ധതി.",
            "category": "subsidy",
            "crops": ["നെല്ല്", "പച്ചക്കറികൾ", "കിഴങ്ങ് വർഗ്ഗങ്ങൾ"],
            "districts": ["വയനാട്", "പാലക്കാട്", "കോഴിക്കോട്", "കണ്ണൂർ"],
            "eligibility": "കേരളത്തിൽ താമസിക്കുന്ന ചെറുകിട കർഷകർ.",
            "amount": "ഹെക്ടറിന് ₹50,000 വരെ",
            "status": "സജീവം",
            "deadline": "2025-06-30",
            "link": "https://www.aims.kerala.gov.in/",
            "ai_summary": "🤖 AI സംഗ്രഹം: കൃഷി ചെയ്യാത്ത ഭൂമിയെ കൃഷിയോഗ്യമാക്കുന്നതിന് കർഷകർക്ക് സാമ്പത്തിക സഹായം നൽകുന്ന പദ്ധതിയാണിത്."
        }
    ]
}

@router.get("/schemes")
def get_schemes(
    lang: str = Query("en"),
    district: Optional[str] = Query(None),
    crop: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None)
):
    data = SCHEMES_DATA.get(lang, SCHEMES_DATA["en"])
    
    filtered = []
    for s in data:
        dist_match = not district or district.lower() == "all" or any(district.lower() in d.lower() for d in s["districts"]) or "All Districts" in s["districts"]
        crop_match = not crop or crop.lower() == "all" or any(crop.lower() in c.lower() for c in s["crops"]) or "All Crops" in s["crops"]
        cat_match = not category or category.lower() == "all" or s["category"].lower() == category.lower()
        
        # New text search logic
        query_match = True
        if q:
            query = q.lower()
            query_match = (
                query in s["name"].lower() or 
                query in s["fullName"].lower() or 
                query in s["description"].lower() or
                any(query in c.lower() for c in s["crops"]) or
                any(query in d.lower() for d in s["districts"])
            )
        
        if dist_match and crop_match and cat_match and query_match:
            filtered.append(s)
            
    return filtered

import httpx
from app.core.config import settings

@router.get("/news")
async def get_news(location: str = "India", lang: str = "en"):
    query_map = {
        "en": "agriculture",
        "ml": "കൃഷി",
        "ta": "விவசாயம்",
        "hi": "कृषि"
    }
    q = query_map.get(lang, "agriculture")
    query = f"{q} {location}"
    
    # We'll simulate AI summary for news in the frontend or pre-fill it here
    if settings.NEWS_API_KEY:
        try:
            url = f"https://newsapi.org/v2/everything?q={query}&apiKey={settings.NEWS_API_KEY}&pageSize=5"
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                data = resp.json()
                articles = data.get("articles", [])
                if data.get("status") == "ok" and len(articles) > 0:
                    return [
                        {
                            "id": i,
                            "title": a["title"], 
                            "content": a["description"] or "Read more for full details.",
                            "date": a["publishedAt"][:10], 
                            "url": a["url"],
                            "category": "news",
                            "ai_summary": f"🤖 AI INSIGHT: {a['title'][:50]}... affects regional farming protocols. Stay updated."
                        } for i, a in enumerate(articles)
                    ]
        except Exception as e:
            print(f"News API Error: {e}")

    # Fallback / Mock Data
    fallbacks = {
        "en": [ 
            {
                "id": 101, 
                "title": f"New Irrigation Project in {location}", 
                "content": "Government approves ₹200Cr for modernization of irrigation canals.", 
                "date": "2024-12-22", 
                "category": "equipment",
                "url": "#",
                "ai_summary": "🤖 AI INSIGHT: This project will improve water accessibility for over 5,000 farmers in the region."
            }, 
            {
                "id": 102, 
                "title": f"Bumper Harvest Expected", 
                "content": "Agriculture department predicts record-breaking paddy harvest this season.", 
                "date": "2024-12-21", 
                "category": "subsidy",
                "url": "#",
                "ai_summary": "🤖 AI INSIGHT: Favorable weather conditions have significantly boosted yield projections."
            } 
        ],
        # ... other languages can be added similarly
    }
    return fallbacks.get(lang, fallbacks["en"])
