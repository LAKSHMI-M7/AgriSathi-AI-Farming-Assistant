import re
import os
import asyncio
from typing import Optional
from app.services.openai_service import get_ai_response
from app.api.routes import weather as weather_route
from app.models.all_models import Document

def detect_intent(text: str) -> str:
    """Layer 1: Precise Intent Detection using Keywords"""
    text = text.lower()

    # Weather
    if any(x in text for x in ["weather", "rain", "forecast", "climate", "monsoon", "mazha", "vanam", "mausam", "barish"]):
        return "weather"
    
    # Irrigation
    if any(x in text for x in ["irrigation", "water", "drip", "sprinkler", "nannayan", "nanaikkum", "sinchai", "paani"]):
        return "irrigation"

    # Fertilizer
    if any(x in text for x in ["fertilizer", "urea", "npk", "manure", "valam", "uram", "khad", "urvarak"]):
        return "fertilizer_advice"

    # Crop Recommendation
    if any(x in text for x in ["recommend", "which crop", "suitable crop", "valarthan", "payirida", "kaunsi fasal", "fasal"]):
        return "crop_recommendation"

    # Disease & Pest
    if any(x in text for x in ["disease", "sick", "leaf spot", "blight", "rogam", "noai", "beemari"]):
        return "disease"
    if any(x in text for x in ["pest", "insect", "bug", "worm", "keedam", "poochi", "keet", "keeda"]):
        return "pest"

    # Soil Health
    if any(x in text for x in ["soil", "ph", "clay", "sand", "mannu", "mitti"]):
        return "soil_health"

    # Crop Rotation
    if any(x in text for x in ["rotation", "cycle", "next crop", "fasal chakra"]):
        return "crop_rotation"

    # Government Schemes & News
    if any(x in text for x in ["scheme", "subsidy", "pm-kisan", "yojana", "pathathi", "thittam", "govt", "sarkari"]):
        return "government_scheme"

    # Market Price
    if any(x in text for x in ["price", "market", "rate", "cost", "vila", "vilai", "daam", "bhaav"]):
        return "market_price"

    # Sowing & Harvesting
    if any(x in text for x in ["sow", "harvest", "plant time", "vithaykkan", "koythu", "buai", "katai"]):
        return "sowing_harvest"

    # Fallback to general farming
    return "general_farming"


async def handle_query(prompt: str, language: str = "en", user_id: Optional[int] = None, db=None) -> str:
    """Layer 2: Intent -> Response Router"""
    intent = detect_intent(prompt)
    
    # Handle greetings ONLY if it's a short standalone greeting (not part of a longer question)
    greetings_keywords = ["hi", "hello", "namaste", "vanakkam", "namaskaram"]
    prompt_lower = prompt.lower().strip()
    
    # Only treat as greeting if message is short (< 20 chars) and contains greeting word
    # OR if the entire message is JUST a greeting word
    is_greeting = False
    if len(prompt_lower) < 20:
        if any(x in prompt_lower for x in greetings_keywords):
            is_greeting = True
    elif prompt_lower in greetings_keywords:
        is_greeting = True
    
    if is_greeting:
        greetings = {
            "en": "Namaste! How can I help you with your farm today?",
            "ta": "வணக்கம்! இன்று உங்கள் பண்ணைக்கு நான் எவ்வாறு உதவ முடியும்?",
            "ml": "നമസ്കാരം! നിങ്ങളുടെ കൃഷിയുമായി ബന്ധപ്പെട്ട് ഇന്ന് എനിക്ക് എങ്ങനെ സഹായിക്കാനാകും?",
            "hi": "नमस्ते! आज मैं आपके खेत में आपकी कैसे मदद कर सकता हूँ?"
        }
        return greetings.get(language, greetings["en"])

    # For specific local data fetching (Weather/Govt), we can wrap AI call or use local logic
    context = ""
    
    if intent == "weather":
        try:
            # Default to Kerala lat/lon
            data = await weather_route.get_weather(lang=language)
            if data:
                summary = data.get('summary', '')
                temp = data.get('temp', '')
                humid = data.get('humidity', '')
                advisory = data.get('advisory', {})
                
                # Create a concise but detailed context for the AI
                adv_text = ". ".join([v['text'] for v in advisory.values()])
                context = f"Weather: {summary}, Temp: {temp}C, Humidity: {humid}%. Farming Advisory: {adv_text}"
        except Exception as e:
            print(f"Assistant Weather Context Error: {e}")
            pass

    if intent == "government_scheme":
        # Check if we have documents uploaded by the user to provide context
        if db is not None and user_id is not None:
            docs = db.query(Document).filter(Document.user_id == user_id).all()
            if docs:
                titles = ", ".join([d.filename for d in docs])
                context = f"The farmer has the following documents saved: {titles}. "

    # Route to AI with the detected intent and context
    # The prompt will include the intent to guide the AI format
    ai_prompt = f"Intent: {intent}\nQuestion: {prompt}"
    return get_ai_response(ai_prompt, language, context=context)



    
