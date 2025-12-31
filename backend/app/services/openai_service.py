import openai
from app.core.config import settings
import time
import base64

import google.generativeai as genai
from PIL import Image
import io

# Configure AI Client (Groq)
client = openai.OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def get_ai_response(prompt: str, language: str = "en", context: str = ""):
    brand_names = {
        "en": "AgriSathi",
        "ta": "அக்ரிசாதி",
        "ml": "അഗ്രിസതി",
        "hi": "एग्रीसाथी"
    }
    brand_name = brand_names.get(language, "AgriSathi")

    system_instr = f"""
    ROLE: You are {brand_name}, the expert AI Farming Assistant for Indian farmers.
    
    CRITICAL RULES:
    1. Answer ALL farming-related questions.
    2. LANGUAGE: Respond EXCLUSIVELY in the {language} language. 
    3. DO NOT USE ENGLISH words if a {language} equivalent exists. 
    4. Even technical terms should be described or translated into {language} where possible.
    5. NEVER mix English with {language}. If you are providing a list, every single word must be in {language}.
    
    STRICT ANSWER FORMAT (Must follow this for every response):
    1️⃣ Short Answer: (1–2 lines direct answer)
    2️⃣ Detailed Guidance: (Bulleted practical steps)
    3️⃣ Farmer Tip: (One actionable, pro-tip for better results)

    Context Info: {context}
    """

    # Try Groq
    if settings.GROQ_API_KEY:
        max_retries = 2
        for i in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_instr},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1200,  # Increased for Tamil/Malayalam/Hindi which use more tokens
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI Error: {e}")
                if i < max_retries - 1:
                    time.sleep(2)
                else:
                    break

    # Fallback to Rule-Based / Mock
    return get_mock_response(prompt, language)


def get_mock_response(prompt: str, language: str = "en") -> str:
    prompt_l = prompt.lower()
    
    # Generic templates based on language
    templates = {
        "en": {
            "paddy": "1️⃣ Short Answer: Best for Kerala's wetlands.\n2️⃣ Detailed Guidance:\n• Use CO-51 variety.\n• Maintain 2cm water.\n• Apply NPK 100:50:50.\n3️⃣ Farmer Tip: Use azolla to fix nitrogen naturally.",
            "coconut": "1️⃣ Short Answer: Ideal for coastal sandy soil.\n2️⃣ Detailed Guidance:\n• Space 7.5m apart.\n• Apply salt and ash.\n• Watch for Red Palm Weevil.\n3️⃣ Farmer Tip: Intercrop with cocoa or pepper for extra income.",
            "weather": "1️⃣ Short Answer: Expect moderate rain this week.\n2️⃣ Detailed Guidance:\n• Temp: 27°C-31°C.\n• Humidity: High.\n• Winds: Moderate.\n3️⃣ Farmer Tip: Check drainage channels to avoid waterlogging.",
            "default": "1️⃣ Short Answer: AgriSathi is here to help with your farm.\n2️⃣ Detailed Guidance:\n• Focus on seasonal crops.\n• Use organic fertilizers where possible.\n• Monitor for early signs of pests.\n3️⃣ Farmer Tip: Regularly test your soil at the local Krishi Bhavan."
        },
        "ml": {
            "paddy": "1️⃣ ചുരുങ്ങിയ മറുപടി: കേരളത്തിലെ തണ്ണീർത്തടങ്ങൾക്ക് ഏറ്റവും അനുയോജ്യം.\n2️⃣ വിശദമായ മാർഗ്ഗനിർദ്ദേശങ്ങൾ:\n• CO-51 ഇനം ഉപയോഗിക്കുക.\n• 2 സെന്റിമീറ്റർ വെള്ളം നിലനിർത്തുക.\n• NPK 100:50:50 പ്രയോഗിക്കുക.\n3️⃣ കർഷക ടിപ്പ്: നൈട്രജൻ വർദ്ധിപ്പിക്കാൻ അസോള ഉപയോഗിക്കുക.",
            "default": "1️⃣ ചുരുങ്ങിയ മറുപടി: നിങ്ങളുടെ കൃഷിയെ സഹായിക്കാൻ അഗ്രിസതി സന്നദ്ധമാണ്.\n2️⃣ വിശദമായ മാർഗ്ഗനിർദ്ദേശങ്ങൾ:\n• കാലാവസ്ഥയ്ക്ക് അനുയോജ്യമായ വിളകൾ തിരഞ്ഞെടുക്കുക.\n• ജൈവവളങ്ങൾ ഉപയോഗിക്കാൻ ശ്രദ്ധിക്കുക.\n• കീടങ്ങളെ നേരത്തെ തിരിച്ചറിഞ്ഞ് പ്രതിരോധിക്കുക.\n3️⃣ കർഷക ടിപ്പ്: കൃഷിഭവനിൽ പോയി കൃത്യസമയത്ത് മണ്ണ് പരിശോധിക്കുക."
        },
        "ta": {
            "paddy": "1️⃣ குறுகிய பதில்: நெல் சாகுபடிக்கு ஈரநிலங்கள் மிகவும் ஏற்றவை.\n2️⃣ விரிவான வழிகாட்டுதல்:\n• CO-51 ரகத்தைப் பயன்படுத்தவும்.\n• நிலத்தில் 2 செமீ தண்ணீரைத் தேக்கி வைக்கவும்.\n• NPK 100:50:50 உரமிடவும்.\n3️⃣ விவசாய உதவிக்குறிப்பு: தழைச்சத்தை அதிகரிக்க அசோலாவைப் பயன்படுத்தவும்.",
            "default": "1️⃣ குறுகிய பதில்: அக்ரிசாதி உங்கள் விவசாயத்திற்கு உதவ தயாராக உள்ளது.\n2️⃣ விரிவான வழிகாட்டுதல்:\n• பருவகாலத்திற்கு ஏற்ற பயிர்களைத் தேர்ந்தெடுக்கவும்.\n• இயற்கை உரங்களைப் பயன்படுத்த முன்னுரிமை அளிக்கவும்.\n• பூச்சிக் கிருமிகளைக் கண்காணித்து உடனுக்குடன் நடவடிக்கை எடுக்கவும்.\n3️⃣ விவசாய உதவிக்குறிப்பு: உங்கள் மண்ணை வேளாண் மையத்தில் கொடுத்து பரிசோதிக்கவும்."
        },
        "hi": {
            "paddy": "1️⃣ लघु उत्तर: धान की खेती के लिए आर्द्रभूमि सबसे अच्छी है।\n2️⃣ विस्तृत मार्गदर्शन:\n• CO-51 किस्म का उपयोग करें।\n• खेत में 2 सेमी पानी बनाए रखें।\n• NPK 100:50:50 उर्वरक का प्रयोग करें।\n3️⃣ किसान टिप: नाइट्रोजन बढ़ाने के लिए अजोला का उपयोग करें।",
            "default": "1️⃣ लघु उत्तर: एग्रीसाथी आपकी खेती में मदद करने के लिए तैयार है।\n2️⃣ विस्तृत मार्गदर्शन:\n• मौसमी फसलों पर ध्यान दें।\n• जैविक उर्वरकों का प्रयोग करें।\n• कीटों के शुरुआती लक्षणों की निगरानी करें।\n3️⃣ किसान टिप: अपने मिट्टी की नियमित रूप से केंद्र पर जांच कराएं।"
        }
    }

    lang_templates = templates.get(language, templates["en"])
    
    if "paddy" in prompt_l or "rice" in prompt_l or "nellu" in prompt_l:
        return lang_templates.get("paddy", lang_templates["default"])
    if "coconut" in prompt_l or "thethe" in prompt_l:
        return lang_templates.get("coconut", lang_templates["default"])
    if "weather" in prompt_l or "rain" in prompt_l:
        return lang_templates.get("weather", lang_templates["default"])
        
    return lang_templates["default"]

def generate_roadmap(goal: str, language: str = "en"):
    prompt = f"Create a step-by-step farming roadmap for: {goal}. Respond in {language}."
    return get_ai_response(prompt, language)

def generate_crop_advice(params: dict, crop: str, language: str = "en"):
    """
    Generates dynamic AI advice for a specific crop and soil/weather context.
    """
    prompt = f"""
    ANALYSIS REQUEST:
    Crop: {crop}
    Parameters: {params}
    Language: {language}

    Please provide:
    1. Weather Warning (Short, actionable)
    2. Soil Health Status (Status word and 1 line description)
    3. Targeted Fertilizer & Correction Advice (Specific steps for N, P, K and pH correction)

    Respond ONLY in the {language} language. Use the exact bullet points: 
    - Weather Warning: 
    - Soil Health: 
    - Advice: 
    """
    # We use a lower temperature for technical advice to keep it grounded
    brand_names = {"en": "AgriSathi", "ta": "அக்ரிசாதி", "ml": "അഗ്രിസതി", "hi": "एग्रीसाथी"}
    brand_name = brand_names.get(language, "AgriSathi")
    
    system_instr = f"You are {brand_name}, an expert agronomist. Provide precise, scientific farming advice in {language}."
    
    if settings.GROQ_API_KEY:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_instr},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,  # Increased for Indian languages
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception:
            pass
            
    return "AI advice temporarily unavailable."

def diagnose_leaf(image_bytes: bytes, language: str = "en"):
    """
    Analyzes leaf image using Google Gemini Flash and returns structured diagnosis.
    """
    if not settings.GEMINI_API_KEY:
        return None

    brand_names = {"en": "AgriSathi", "ta": "அக்ரிசாதி", "ml": "അഗ്രിസതി", "hi": "एग्रीसाथी"}
    brand_name = brand_names.get(language, "AgriSathi")

    prompt = f"""
    You are {brand_name}, an expert AI Plant Pathologist.
    Analyze the attached image and identify if the plant leaf has any disease.
    
    Response MUST be in EXACTLY this format in {language} language:
    Crop: (Name of the crop)
    Disease: (Name of the disease)
    Cure: (Chemical or organic medicine/treatment)
    Cause: (Reason for disease)
    Tip: (Actionable tip to prevent in future)
    
    If no disease is found, state that the plant is healthy.
    Respond ONLY in {language}.
    """

    try:
        # Load image for Gemini
        image = Image.open(io.BytesIO(image_bytes))
        
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content([prompt, image])
        
        return response.text
    except Exception as e:
        print(f"Gemini Vision Error: {e}")
        return None
