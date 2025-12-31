from gtts import gTTS
import os
import uuid

def generate_audio(text: str, lang: str = 'ml'):
    try:
        # Default to Hindi if Malayalam not robust, but gTTS supports 'ml'
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join("app", "static", "uploads", filename)
        tts.save(filepath)
        return f"/static/uploads/{filename}"
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
