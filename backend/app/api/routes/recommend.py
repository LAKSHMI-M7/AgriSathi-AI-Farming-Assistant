from fastapi import APIRouter, Query
from pydantic import BaseModel
import pickle
import os
import pandas as pd
from app.services.openai_service import generate_crop_advice

router = APIRouter()

class CropInput(BaseModel):
    N: float
    P: float
    K: float
    ph: float
    rainfall: float
    temperature: float
    humidity: float

RECOM_DATA = {
    "en": {
        "rice": {
            "name": "Rice (Paddy)",
            "desc": "High rainfall detected, suitable for paddy cultivation.",
            "weather_warning": "Watch for flash floods in low-lying fields.",
            "soil_tip": "Keep soil flooded for better yield."
        },
        "paddy": { # Mapping paddy to rice for consistency
            "name": "Rice (Paddy)",
            "desc": "High rainfall detected, suitable for paddy cultivation.",
            "weather_warning": "Watch for flash floods in low-lying fields.",
            "soil_tip": "Keep soil flooded for better yield."
        },
        "groundnut": {
            "name": "Groundnut",
            "desc": "Best for semi-arid regions with well-drained soil.",
            "weather_warning": "Heavy rain during harvest can cause damage.",
            "soil_tip": "Ensure soil is loose for better pod development."
        },
        "maize": {
            "name": "Maize",
            "desc": "Versatile crop, requires good sunlight and drainage.",
            "weather_warning": "Strong winds can cause lodging.",
            "soil_tip": "Apply Nitrogen in split doses."
        },
        "cotton": {
            "name": "Cotton",
            "desc": "Hot and dry conditions are good for cotton.",
            "weather_warning": "Intense heat might require drip irrigation.",
            "soil_tip": "Ensure good drainage to prevent root rot."
        },
        "jute": {
            "name": "Jute",
            "desc": "Requires humid climate and standing water for retting.",
            "weather_warning": "Early monsoon is beneficial.",
            "soil_tip": "Needs alluvial silty loam soil."
        },
        "coffee": {
            "name": "Coffee",
            "desc": "Best grown under shade in hilly tracts.",
            "weather_warning": "Avoid drought during flowering.",
            "soil_tip": "Maintain high organic matter in soil."
        },
        "tea": {
            "name": "Tea",
            "desc": "Acidic soil and hilly terrain are suitable for tea.",
            "weather_warning": "Heavy mist can affect leaf quality.",
            "soil_tip": "Apply mulch to maintain moisture."
        },
        "general": {
            "name": "Maize / Vegetables",
            "desc": "Moderate conditions suitable for general crops.",
            "weather_warning": "No extreme weather predicted.",
            "soil_tip": "Crop rotation will improve soil fertility."
        },
        "fertilizers": {
            "low_n": "Add 50kg/acre of Urea to boost Nitrogen level.",
            "low_p": "Add 30kg/acre of DAP (Diammonium Phosphate).",
            "low_k": "Add 25kg/acre of MOP (Muriate of Potash).",
            "acidic": "Apply 1 ton/acre of Lime to neutralize acidity.",
            "alkaline": "Apply Gypsum or Sulfur to reduce alkalinity.",
            "healthy": "Soil nutrients are balanced. Use organic compost."
        }
    },
    "ml": {
        "rice": {
            "name": "നെല്ല്",
            "desc": "കൂടുതൽ മഴ ലഭിക്കുന്നതിനാൽ നെൽകൃഷിക്ക് അനുയോജ്യമാണ്.",
            "weather_warning": "താഴ്ന്ന പ്രദേശങ്ങളിൽ വെള്ളപ്പൊക്കം ശ്രദ്ധിക്കുക.",
            "soil_tip": "മികച്ച വിളവിനായി മണ്ണിൽ എപ്പോഴും വെള്ളം നിലനിർത്തുക."
        },
        "cotton": {
            "name": "പരുത്തി",
            "desc": "ചൂടുള്ളതും ഉണങ്ങിയതുമായ കാലാവസ്ഥ പരുത്തിക്ക് നല്ലതാണ്.",
            "weather_warning": "അമിതമായ ചൂടുണ്ടെങ്കിൽ തുള്ളിനന (Drip Irrigation) ആവശ്യമായി വന്നേക്കാം.",
            "soil_tip": "വേര് ചീയുന്നത് തടയാൻ നല്ല നീർവാർച്ച ഉറപ്പാക്കുക."
        },
        "tea": {
            "name": "തേയില",
            "desc": "അമ്ലഗുണമുള്ള മണ്ണും മലനിരകളും തേയില കൃഷിക്ക് അനുയോജ്യമാണ്.",
            "weather_warning": "അമിതമായ മൂടൽമഞ്ഞ് ഇലയുടെ ഗുണനിലവാരത്തെ ബാധിച്ചേക്കാം.",
            "soil_tip": "ഈർപ്പം നിലനിർത്താൻ പുതയിടൽ (Mulching) നടത്തുക."
        },
        "general": {
            "name": "ചോളം / പച്ചക്കറികൾ",
            "desc": "മിതമായ സാഹചര്യങ്ങൾ പൊതുവായ വിളകൾക്ക് അനുയോജ്യമാണ്.",
            "weather_warning": "പ്രത്യേക പ്രതികൂല കാലാവസ്ഥാ മുന്നറിയിപ്പുകളില്ല.",
            "soil_tip": "വിളമാറ്റം മണ്ണിന്റെ ഫലഭൂയിഷ്ഠത വർദ്ധിപ്പിക്കും."
        },
        "fertilizers": {
            "low_n": "നൈട്രജൻ വർദ്ധിപ്പിക്കാൻ ഏക്കറിന് 50 കിലോ യൂറിയ ചേർക്കുക.",
            "low_p": "ഏക്കറിന് 30 കിലോ ഡിഎപി (DAP) ചേർക്കുക.",
            "low_k": "ഏക്കറിന് 25 കിലോ എംഒപി (Potash) ചേർക്കുക.",
            "acidic": "മണ്ണിന്റെ പുളിപ്പ് കുറയ്ക്കാൻ ഏക്കറിന് 1 ടൺ കുമ്മായം ചേർക്കുക.",
            "alkaline": "ക്ഷാരഗുണം കുറയ്ക്കാൻ ജിപ്സം അല്ലെങ്കിൽ സൾഫർ ഉപയോഗിക്കുക.",
            "healthy": "മണ്ണിലെ മൂലകങ്ങൾ സന്തുലിതമാണ്. ജൈവവളം ഉപയോഗിക്കുക."
        }
    },
    "ta": {
        "rice": {
            "name": "நெல்",
            "desc": "அதிக மழை பெய்ய வாய்ப்புள்ளதால் நெல் சாகுபடிக்கு ஏற்றது.",
            "weather_warning": "தாழ்வான பகுதிகளில் வெள்ளம் குறித்து எச்சரிக்கையாக இருக்கவும்.",
            "soil_tip": "சிறந்த மகசூலுக்கு நிலத்தில் எப்போதும் தண்ணீர் இருக்குமாறு பார்த்துக்கொள்ளவும்."
        },
        "cotton": {
            "name": "பருத்தி",
            "desc": "வெப்பமான மற்றும் வறண்ட நிலை பருத்திக்கு நல்லது.",
            "weather_warning": "அதிக வெப்பம் இருந்தால் சொட்டு நீர் பாசனம் தேவைப்படலாம்.",
            "soil_tip": "வேர் அழுகலைத் தடுக்க முறையான வடிகால் வசதியை உறுதி செய்யவும்."
        },
        "tea": {
            "name": "தேயிலை",
            "desc": "அமிலத்தன்மை கொண்ட மண் தேயிலை பயிரிட ஏற்றது.",
            "weather_warning": "அதிக மூடுபனி இலைகளின் தரத்தை பாதிக்கலாம்.",
            "soil_tip": "ஈரப்பதத்தை பராமரிக்க மூடாக்கு (Mulch) போடவும்."
        },
        "general": {
            "name": "சோளம் / காய்கறிகள்",
            "desc": "மிதமான நிலைமைகள் மற்ற பயிர்களுக்கு ஏற்றது.",
            "weather_warning": "மோசமான வானிலை முன்னறிவிப்பு ஏதுமில்லை.",
            "soil_tip": "பயிர் சுழற்சி மண்ணின் வளத்தை மேம்படுத்தும்."
        },
        "fertilizers": {
            "low_n": "நைட்ரஜனை அதிகரிக்க ஏக்கருக்கு 50 கிலோ யூரியா சேர்க்கவும்.",
            "low_p": "ஏக்கருக்கு 30 கிலோ டிஏபி (DAP) சேர்க்கவும்.",
            "low_k": "ஏக்கருக்கு 25 கிலோ பொட்டாஷ் சேர்க்கவும்.",
            "acidic": "மண்ணின் அமிலத்தன்மையை சமநிலைப்படுத்த ஏக்கருக்கு 1 டன் சுண்ணாம்பு சேர்க்கவும்.",
            "alkaline": "ஜிப்சம் அல்லது கந்தகம் பயன்படுத்தி காரத்தன்மையைக் குறைக்கவும்.",
            "healthy": "மண்ணில் சத்துக்கள் சமமாக உள்ளன. இயற்கை உரங்களைப் பயன்படுத்தவும்."
        }
    },
    "hi": {
        "rice": {
            "name": "चावल (धान)",
            "desc": "अधिक वर्षा होने के कारण धान की खेती के लिए उपयुक्त।",
            "weather_warning": "निचले खेतों में बाढ़ की स्थिति पर नज़र रखें।",
            "soil_tip": "बेहतर उपज के लिए खेत में पानी भरकर रखें।"
        },
        "paddy": {
            "name": "चावल (धान)",
            "desc": "अधिक वर्षा होने के कारण धान की खेती के लिए उपयुक्त।",
            "weather_warning": "निचले खेतों में बाढ़ की स्थिति पर नज़र रखें।",
            "soil_tip": "बेहतर उपज के लिए खेत में पानी भरकर रखें।"
        },
        "groundnut": {
            "name": "मूंगफली",
            "desc": "अच्छी जल निकासी वाली मिट्टी और अर्ध-शुष्क क्षेत्रों के लिए सर्वोत्तम।",
            "weather_warning": "कटाई के दौरान भारी बारिश नुकसान पहुंचा सकती है।",
            "soil_tip": "बेहतर फली विकास के लिए मिट्टी ढीली रखें।"
        },
        "maize": {
            "name": "मक्का",
            "desc": "बहुमुखी फसल, इसके लिए अच्छी धूप और जल निकासी की आवश्यकता होती है।",
            "weather_warning": "तेज हवाएं फसल गिरने का कारण बन सकती हैं।",
            "soil_tip": "नाइट्रोजन का प्रयोग अलग-अलग खुराक में करें।"
        },
        "cotton": {
            "name": "कपास",
            "desc": "गर्म और शुष्क स्थितियां कपास के लिए अच्छी होती हैं।",
            "weather_warning": "अत्यधिक गर्मी के कारण ड्रिप सिंचाई की आवश्यकता हो सकती है।",
            "soil_tip": "जड़ सड़न रोकने के लिए जल निकासी की अच्छी व्यवस्था करें।"
        },
        "jute": {
            "name": "जूट",
            "desc": "सड़ने के लिए आर्द्र जलवायु और खड़े पानी की आवश्यकता होती है।",
            "weather_warning": "शुरुआती मानसून फायदेमंद होता है।",
            "soil_tip": "जलोढ़ रेतीली दोमट मिट्टी की आवश्यकता होती है।"
        },
        "coffee": {
            "name": "कॉफी",
            "desc": "पहाड़ी इलाकों में छाया के नीचे सबसे अच्छी तरह उगाई जाती है।",
            "weather_warning": "फूल आने के दौरान सूखे से बचें।",
            "soil_tip": "मिट्टी में उच्च कार्बनिक पदार्थ बनाए रखें।"
        },
        "tea": {
            "name": "चाय",
            "desc": "अम्लीय मिट्टी और पहाड़ी क्षेत्र चाय के लिए उपयुक्त हैं।",
            "weather_warning": "भारी धुंध पत्तों की गुणवत्ता को प्रभावित कर सकती है।",
            "soil_tip": "नमी बनाए रखने के लिए मल्चिंग करें।"
        },
        "general": {
            "name": "मक्का / सब्जियां",
            "desc": "सामान्य फसलों के लिए उपयुक्त मध्यम स्थितियां।",
            "weather_warning": "किसी खराब मौसम की भविष्यवाणी नहीं की गई है।",
            "soil_tip": "फसल चक्र से मिट्टी की उर्वरता बढ़ेगी।"
        },
        "fertilizers": {
            "low_n": "नाइट्रोजन बढ़ाने के लिए प्रति एकड़ 50 किलो यूरिया डालें।",
            "low_p": "प्रति एकड़ 30 किलो डीएपी (DAP) डालें।",
            "low_k": "प्रति एकड़ 25 किलो एमओपी (Potash) डालें।",
            "acidic": "अम्लता कम करने के लिए प्रति एकड़ 1 टन चूना डालें।",
            "alkaline": "क्षारीयता कम करने के लिए जिप्सम या सल्फर का प्रयोग करें।",
            "healthy": "मिट्टी के पोषक तत्व संतुलित हैं। जैविक खाद का प्रयोग करें।"
        }
    }
}

# Load the trained AI model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "crop_model.pkl")
model = None

def get_model():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
    return model

@router.post("/recommend")
def recommend_crop(data: CropInput, lang: str = Query("en")):
    t = RECOM_DATA.get(lang, RECOM_DATA["en"])
    f = t["fertilizers"]
    
    # AI Prediction Logic
    ai_model = get_model()
    if ai_model:
        # Create input for model
        input_df = pd.DataFrame([[
            data.N, data.P, data.K, data.ph, data.temperature, data.rainfall, data.humidity
        ]], columns=['N', 'P', 'K', 'pH', 'temp', 'rainfall', 'humidity'])
        
        prediction = ai_model.predict(input_df)[0]
        best_crop = t.get(prediction, t["general"])
    else:
        # Rule-based fallback if model is missing
        crops = []
        if data.rainfall > 200: crops.append(t["rice"])
        if data.temperature > 30: crops.append(t["cotton"])
        if data.ph < 5.5: crops.append(t["tea"])
        best_crop = crops[0] if crops else t["general"]
    
    # Dynamic AI Advice
    params = {
        "N": data.N, "P": data.P, "K": data.K, 
        "pH": data.ph, "temp": data.temperature, 
        "rainfall": data.rainfall, "humidity": data.humidity
    }
    
    ai_advice_raw = generate_crop_advice(params, best_crop["name"], lang)
    
    # Parse AI response
    weather_warn = best_crop["weather_warning"]
    soil_status_text = "Healthy" if data.ph >= 6 and data.ph <= 7 else "Needs Correction"
    advice_list = []
    
    if ai_advice_raw and "AI advice temporarily unavailable" not in ai_advice_raw:
        lines = ai_advice_raw.split('\n')
        for line in lines:
            if "Weather Warning:" in line:
                weather_warn = line.split("Weather Warning:")[1].strip()
            elif "Soil Health:" in line:
                soil_status_text = line.split("Soil Health:")[1].strip()
            elif "Advice:" in line:
                # Advice might be multiple lines or a single line
                advice_list.append(line.split("Advice:")[1].strip())
            elif line.strip().startswith("- ") or line.strip().startswith("• "):
                advice_list.append(line.strip()[2:])
    
    # Fallback to static if parsing fails or list empty
    if not advice_list:
        if data.N < 50: advice_list.append(f["low_n"])
        if data.P < 30: advice_list.append(f["low_p"])
        if data.K < 30: advice_list.append(f["low_k"])
        if data.ph < 5.8: advice_list.append(f["acidic"])
        elif data.ph > 7.5: advice_list.append(f["alkaline"])
        if not advice_list: advice_list.append(f["healthy"])

    return {
        "recommended_crop": best_crop["name"],
        "description": best_crop["desc"],
        "weather_warning": weather_warn,
        "soil_tip": best_crop["soil_tip"],
        "fertilizer_advice": advice_list,
        "soil_status": soil_status_text
    }
