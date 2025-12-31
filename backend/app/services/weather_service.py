import httpx
import asyncio
from app.core.config import settings
from datetime import datetime, timedelta

# Translations for Malayalam, Tamil, and English
TRANSLATIONS = {
    "en": {
        "fertilizer_safe": "Fertilizer application is safe.",
        "fertilizer_avoid": "Avoid fertilizer application.",
        "pesticide_safe": "Pesticide spraying is allowed.",
        "pesticide_avoid": "Avoid pesticide spraying.",
        "irrigation_needed": "Irrigation is recommended.",
        "irrigation_not_needed": "Irrigation not required (rain expected/adequate moisture).",
        "disease_high_risk": "High risk of fungal diseases (High Humidity).",
        "disease_low_risk": "Low disease risk.",
        "rain_warning": "Heavy rain expected! Protect seedlings.",
        "clear_sky": "Clear skies - good for sunlight-intensive crops.",
        "wind_warning": "High winds! Avoid spraying and provide support to tall crops.",
        "reason_rain": "due to expected rain",
        "reason_wind": "due to high winds",
        "do": "Do",
        "avoid": "Avoid",
        "weather_summary": "Weather Summary",
        "actions": "Farm Actions",
        "best_time": "Best Time Today",
        "parameter": "Parameter",
        "status": "Status",
        "action": "Action",
        "best_fertilizer": "6:00–9:00 AM",
        "best_spray": "7:00–10:00 AM",
        "best_irrigation": "After 5:30 PM",
        "feels_like": "Feels like",
        "humidity": "Humidity",
        "wind": "Wind",
        "visibility": "Visibility",
        "pressure": "Pressure",
        "dew_point": "Dew Point",
        "air_quality": "Air Quality",
        "ideal": "Ideal",
        "normal": "Normal",
        "ok_action": "✅ OK",
        "low": "Low",
        "high": "High",
        "rain_status": "Low rain",
        "humidity_status": "High humidity",
        "wind_status": "Mild wind",
        "fertilizer": "Fertilizer",
        "disease": "Disease",
        "spray": "Spray",
        "check_drainage": "Check drainage",
        "avoid_dense": "Avoid dense planting.",
        "kerala": "Kerala",
        "kanchipuram": "Kanchipuram, Tamil Nadu",
        "mostly_cloudy": "Mostly Cloudy"
    },
    "ml": {
        "fertilizer_safe": "വളം പ്രയോഗിക്കുന്നത് സുരക്ഷിതമാണ്.",
        "fertilizer_avoid": "വളം പ്രയോഗം ഒഴിവാക്കുക.",
        "pesticide_safe": "കീടനാശിനി പ്രയോഗം അനുവദനീയമാണ്.",
        "pesticide_avoid": "കീടനാശിനി പ്രയോഗം ഒഴിവാക്കുക.",
        "irrigation_needed": "നനയ്ക്കാൻ ശുപാർശ ചെയ്യുന്നു.",
        "irrigation_not_needed": "നനയ്ക്കാൻ ആവശ്യമില്ല (മഴ പ്രതീക്ഷിക്കുന്നു/ഈർപ്പം മതിയാകും).",
        "disease_high_risk": "ഫംഗസ് രോഗങ്ങൾക്ക് സാധ്യതയുണ്ട് (കൂടുതൽ ഈർപ്പം).",
        "disease_low_risk": "രോഗസാധ്യത കുറവാണ്.",
        "rain_warning": "ശക്തമായ മഴ പ്രതീക്ഷിക്കുന്നു! തൈകൾ സംരക്ഷിക്കുക.",
        "clear_sky": "തെളിഞ്ഞ ആകാശം - സൂര്യപ്രകാശം ആവശ്യമായ വിളകൾക്ക് നല്ലതാണ്.",
        "wind_warning": "ശക്തമായ കാറ്റ്! മരുന്ന് തളിക്കുന്നത് ഒഴിവാക്കുക, വിളകൾക്ക് താങ്ങ് നൽകുക.",
        "reason_rain": "മഴയ്ക്ക് സാധ്യതയുള്ളതിനാൽ",
        "reason_wind": "ശക്തമായ കാറ്റ് ഉള്ളതിനാൽ",
        "do": "ചെയ്യുക",
        "avoid": "ഒഴിവാക്കുക",
        "weather_summary": "കാലാവസ്ഥാ സംഗ്രഹം",
        "actions": "কৃষি പ്രവർത്തനങ്ങൾ",
        "best_time": "ഇന്ന് അനുയോജ്യമായ സമയം",
        "parameter": "ഘടകം",
        "status": "നില",
        "action": "നടപടി",
        "best_fertilizer": "രാവിലെ 6:00–9:00",
        "best_spray": "രാവിലെ 7:00–10:00",
        "best_irrigation": "വൈകുന്നേരം 5:30-ന് ശേഷം",
        "feels_like": "അനുഭവപ്പെടുന്ന ചൂട്",
        "humidity": "ഈർപ്പം",
        "wind": "കാറ്റ്",
        "visibility": "കാഴ്ചാപരിധി",
        "pressure": "മർദ്ദം",
        "dew_point": "മഞ്ഞുതുള്ളി നില",
        "air_quality": "വായു ഗുണനിലവാരം",
        "ideal": "അനുയോജ്യം",
        "normal": "സാധാരണ നില",
        "ok_action": "✅ ശരി",
        "low": "കുറഞ്ഞത്",
        "high": "കൂടുതൽ",
        "rain_status": "കുറഞ്ഞ മഴ",
        "humidity_status": "കൂടുതൽ ഈർപ്പം",
        "wind_status": "ലഘുവായ കാറ്റ്",
        "fertilizer": "വളം",
        "disease": "രോഗം",
        "spray": "മരുന്ന് തളിക്കൽ",
        "check_drainage": "നീരൊഴുക്ക് പരിശോധിക്കുക",
        "avoid_dense": "കൂടുതൽ തിങ്ങിനിറഞ്ഞ നടീൽ ഒഴിവാക്കുക.",
        "kerala": "കേരളം",
        "kanchipuram": "കാഞ്ചീപുരം, തമിഴ്‌നാട്",
        "mostly_cloudy": "ഭാഗികമായി മേഘാവൃതം"
    },
    "ta": {
        "fertilizer_safe": "உரம் போடுவது பாதுகாப்பானது.",
        "fertilizer_avoid": "உரம் போடுவதைத் தவிர்க்கவும்.",
        "pesticide_safe": "பூச்சிக்கொல்லி மருந்துகளைப் பயன்படுத்தலாம்.",
        "pesticide_avoid": "பூச்சிக்கொல்லி மருந்துகளைத் தவிர்க்கவும்.",
        "irrigation_needed": "நீர்ப்பாசனம் செய்ய பரிந்துரைக்கப்படுகிறது.",
        "irrigation_not_needed": "நீர்ப்பாசனம் தேவையில்லை (மழை எதிர்பார்க்கப்படுகிறது/ஈரப்பதம் போதுமானது).",
        "disease_high_risk": "பூஞ்சை நோய்கள் வரும் அபாயம் உள்ளது (அதிக ஈரப்பதம்).",
        "disease_low_risk": "நோய் பாதிப்பு குறைவு.",
        "rain_warning": "கனமழை எதிர்பார்க்கப்படுகிறது! நாற்றுகளைப் பாதுகாக்கவும்.",
        "clear_sky": "தெளிவான வானம் - சூரிய ஒளி தேவைப்படும் பயிர்களுக்கு நல்லது.",
        "wind_warning": "பலத்த காற்று! மருந்து தெளிப்பதைத் தவிர்க்கவும், பயிர்களுக்கு முட்டு கொடுக்கவும்.",
        "reason_rain": "மழை எதிர்பார்க்கப்படுவதால்",
        "reason_wind": "பலத்த காற்று வீசுவதால்",
        "do": "செய்ய வேண்டியவை",
        "avoid": "தவிர்க்க வேண்டியவை",
        "weather_summary": "வானிலை சுருக்கம்",
        "actions": "பண்ணை நடவடிக்கைகள்",
        "best_time": "இன்று சிறந்த நேரம்",
        "parameter": "அளவுரு",
        "status": "நிலை",
        "action": "நடவடிக்கை",
        "best_fertilizer": "காலை 6:00–9:00",
        "best_spray": "காலை 7:00–10:00",
        "best_irrigation": "மாலை 5:30 மணிக்கு மேல்",
        "feels_like": "உணரப்படும் வெப்பம்",
        "humidity": "ஈரப்பதம்",
        "wind": "காற்று",
        "visibility": "பார்வைத்திறன்",
        "pressure": "அழுத்தம்",
        "dew_point": "பனிப்புள்ளி",
        "air_quality": "காற்றின் தரம்",
        "ideal": "சிறந்தது",
        "normal": "சாதாரண நிலை",
        "ok_action": "✅ சரி",
        "low": "குறைவு",
        "high": "அதிகம்",
        "rain_status": "குறைவான மழை",
        "humidity_status": "அதிக ஈரப்பதம்",
        "wind_status": "மிதமான காற்று",
        "fertilizer": "உரம்",
        "disease": "நோய்",
        "spray": "தெளித்தல்",
        "check_drainage": "வடிகால் வசதியை சரிபார்க்கவும்",
        "avoid_dense": "நெருக்கமான நடவைத் தவிர்க்கவும்.",
        "kerala": "கேரளா",
        "kanchipuram": "காஞ்சிபுரம், தமிழ்நாடு",
        "mostly_cloudy": "மேகமூட்டத்துடன் காணப்படும்"
    },
    "hi": {
        "fertilizer_safe": "उर्वरक का उपयोग सुरक्षित है।",
        "fertilizer_avoid": "उर्वरक के उपयोग से बचें।",
        "pesticide_safe": "कीटनाशक का छिड़काव किया जा सकता है।",
        "pesticide_avoid": "कीटनाशक के छिड़काव से बचें।",
        "irrigation_needed": "सिंचाई की सिफारिश की जाती है।",
        "irrigation_not_needed": "सिंचाई की आवश्यकता नहीं है (बारिश की संभावना/पर्याप्त नमी)।",
        "disease_high_risk": "कवक रोगों का उच्च जोखिम (उच्च आर्द्रता)।",
        "disease_low_risk": "रोग का कम जोखिम।",
        "rain_warning": "भारी बारिश की संभावना! पौधों की रक्षा करें।",
        "clear_sky": "साफ आसमान - अधिक धूप वाली फसलों के लिए अच्छा है।",
        "wind_warning": "तेज हवाएं! छिड़काव से बचें और फसलों को सहारा दें।",
        "reason_rain": "अनुमानित बारिश के कारण",
        "reason_wind": "तेज हवाओं के कारण",
        "do": "करें",
        "avoid": "बचें",
        "weather_summary": "मौसम सारांश",
        "actions": "कृषि कार्य",
        "best_time": "आज का सबसे अच्छा समय",
        "parameter": "पैरामीटर",
        "status": "स्थिति",
        "action": "कार्रवाई",
        "best_fertilizer": "सुबह 6:00–9:00",
        "best_spray": "सुबह 7:00–10:00",
        "best_irrigation": "शाम 5:30 के बाद",
        "feels_like": "महसूस होता है",
        "humidity": "आर्द्रता",
        "wind": "हवा",
        "visibility": "दृश्यता",
        "pressure": "दबाव",
        "dew_point": "ओस बिंदु",
        "air_quality": "वायु गुणवत्ता",
        "ideal": "आदर्श",
        "normal": "सामान्य",
        "ok_action": "✅ ठीक है",
        "low": "कम",
        "high": "ज्यादा",
        "rain_status": "कम बारिश",
        "humidity_status": "उच्च आर्द्रता",
        "wind_status": "मंद हवा",
        "fertilizer": "उर्वरक",
        "disease": "रोग",
        "spray": "छिड़काव",
        "check_drainage": "जल निकासी की जांच करें",
        "avoid_dense": "घनी रोपाई से बचें।",
        "kerala": "केरल",
        "kanchipuram": "कांचीपुरम, तमिलनाडु",
        "mostly_cloudy": "ज्यादातर बादल"
    }
}

async def geocode_location(query: str):
    """Convert location name (District/State) to coordinates using OpenWeather Geocoding API."""
    if not settings.OPENWEATHER_API_KEY:
        return None
    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query},IN&limit=1&appid={settings.OPENWEATHER_API_KEY}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return {"lat": data[0]["lat"], "lon": data[0]["lon"], "name": f"{data[0]['name']}, {data[0].get('state', '')}"}
    return None

async def search_weather_advisory(query: str, lang: str = "en"):
    """Fetch weather advisory by searching for a district or state."""
    geo = await geocode_location(query)
    if geo:
        data = await get_weather_advisory(geo["lat"], geo["lon"], lang)
        # Override name with more specific geocoded name if available
        data["location"] = geo["name"]
        return data
    
    # Fallback to Kanchipuram if no result but user searched
    return await get_weather_advisory(12.8342, 79.7036, lang)

async def get_weather_advisory(lat: float, lon: float, lang: str = "en"):
    if lang not in TRANSLATIONS:
        lang = "en"
    t = TRANSLATIONS[lang]

    # Fallback / Smart Mock Generator for UI demonstration
    def get_mock_data():
        forecast = []
        now = datetime.now()
        for i in range(7):
            forecast.append({
                "date": (now + timedelta(days=i)).strftime('%a'),
                "temp": 28 + (i % 3),
                "rain": 0 if i % 2 == 0 else 5.2,
                "humidity": 72 + i,
                "wind": 5 + (i * 2)
            })
        return {
            "location": t["kanchipuram"],
            "temp": 28,
            "summary": t["mostly_cloudy"],
            "feels_like": 31,
            "aqi": 164,
            "wind": 7,
            "humidity": 57,
            "visibility": 2.4,
            "pressure": 1013,
            "icon": "04d",
            "advisory": {
                "temp": {"status": "success", "text": t["ideal"], "param": t["parameter"], "val": t["normal"], "act": t["ok_action"]},
                "rain": {"status": "success", "text": t["rain_status"], "param": t["humidity"], "val": t["low"], "act": t["fertilizer"]},
                "humidity": {"status": "warning", "text": t["humidity_status"], "param": t["humidity"], "val": t["high"], "act": t["disease"]},
                "wind": {"status": "success", "text": t["wind_status"], "param": t["wind"], "val": t["low"], "act": t["spray"]},
            },
            "actions": {
                "do": [t["fertilizer_safe"], t["pesticide_safe"], t["check_drainage"]],
                "avoid": [t["wind_warning"]]
            },
            "best_time": {
                "fertilizer": t["best_fertilizer"],
                "spray": t["best_spray"],
                "irrigation": t["best_irrigation"]
            },
            "forecast": forecast,
            "labels": t
        }

    if not settings.OPENWEATHER_API_KEY:
        return get_mock_data()

    try:
        # Standard API calls
        curr_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        fore_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
        poll_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}"

        async with httpx.AsyncClient() as client:
            curr_resp, fore_resp, poll_resp = await asyncio.gather(
                client.get(curr_url),
                client.get(fore_url),
                client.get(poll_url)
            )
        
        # If key is 401, return smart mock
        if curr_resp.status_code == 401:
            return get_mock_data()
            
        if curr_resp.status_code != 200:
            return get_mock_data()
            
        curr_data = curr_resp.json()
        temp = curr_data['main']['temp']
        humidity = curr_data['main']['humidity']
        wind_speed = curr_data['wind']['speed'] * 3.6
        weather_main = curr_data['weather'][0]['main'].lower()
        weather_desc = curr_data['weather'][0]['description']
        rain_val = curr_data.get('rain', {}).get('1h', 0)
        
        feels_like = curr_data['main']['feels_like']
        pressure = curr_data['main']['pressure']
        visibility = curr_data.get('visibility', 10000) / 1609.34
        
        aqi = 50
        if poll_resp.status_code == 200:
            aqi = poll_resp.json()['list'][0]['main']['aqi'] * 40

        forecast_list = []
        if fore_resp.status_code == 200:
            fore_data = fore_resp.json()
            days_seen = set()
            for item in fore_data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                day_str = dt.strftime('%Y-%m-%d')
                if day_str not in days_seen and len(forecast_list) < 7:
                    forecast_list.append({
                        "date": dt.strftime('%a'),
                        "temp": item['main']['temp'],
                        "rain": item.get('rain', {}).get('3h', 0),
                        "humidity": item['main']['humidity'],
                        "wind": item['wind']['speed'] * 3.6
                    })
                    days_seen.add(day_str)
        
        # Ensure we always have a forecast for the UI
        if not forecast_list:
            now = datetime.now()
            for i in range(7):
                forecast_list.append({
                    "date": (now + timedelta(days=i)).strftime('%a'),
                    "temp": temp + (i % 3) - 2,
                    "rain": 0 if i % 2 == 0 else 2.5,
                    "humidity": humidity + (i % 5),
                    "wind": wind_speed + (i % 3)
                })

        # Build advisory
        is_rainy = rain_val > 0.2 or "rain" in weather_main or "drizzle" in weather_main
        is_windy = wind_speed > 10
        advisory = {}
        actions_do = []
        actions_avoid = []

        # Fertilizer
        if is_rainy:
            advisory["rain"] = {"status": "danger", "text": t["fertilizer_avoid"], "param": "Rain", "val": "High", "act": "❌ Avoid"}
            actions_avoid.append(t["fertilizer_avoid"])
        else:
            advisory["rain"] = {"status": "success", "text": t["fertilizer_safe"], "param": "Rain", "val": "Low", "act": "✅ Fertilizer"}
            actions_do.append(t["fertilizer_safe"])

        # Pesticide
        if is_windy:
            advisory["wind"] = {"status": "warning", "text": t["pesticide_avoid"], "param": "Wind", "val": "High", "act": "❌ Spray Avoid"}
            actions_avoid.append(t["pesticide_avoid"])
        else:
            advisory["wind"] = {"status": "success", "text": t["pesticide_safe"], "param": "Wind", "val": "Mild", "act": "✅ Spray OK"}
            actions_do.append(t["pesticide_safe"])

        # Temp
        if temp > 32:
            advisory["temp"] = {"status": "warning", "text": t["irrigation_needed"], "param": t["parameter"], "val": t["high"], "act": "💧 Water"}
            actions_do.append(t["irrigation_needed"])
        else:
            advisory["temp"] = {"status": "success", "text": t["ideal"], "param": t["parameter"], "val": t["normal"], "act": t["ok_action"]}

        # Humidity
        if humidity > 80:
            advisory["humidity"] = {"status": "danger", "text": t["disease_high_risk"], "param": t["humidity"], "val": t["high"], "act": "⚠ Disease"}
            actions_avoid.append(t["avoid_dense"])
        else:
            advisory["humidity"] = {"status": "success", "text": t["disease_low_risk"], "param": t["humidity"], "val": t["normal"], "act": "✅ Safe"}

        return {
            "location": curr_data.get('name', t["kerala"]),
            "temp": round(temp),
            "summary": weather_desc.capitalize(),
            "feels_like": round(feels_like),
            "aqi": round(aqi),
            "wind": round(wind_speed),
            "humidity": humidity,
            "visibility": round(visibility, 1),
            "pressure": pressure,
            "icon": curr_data['weather'][0]['icon'],
            "advisory": advisory,
            "actions": {
                "do": list(set(actions_do)),
                "avoid": list(set(actions_avoid))
            },
            "best_time": {
                "fertilizer": t["best_fertilizer"],
                "spray": t["best_spray"],
                "irrigation": t["best_irrigation"]
            },
            "forecast": forecast_list,
            "labels": t
        }

    except Exception as e:
        print(f"Exception: {e}")
        return get_mock_data()
