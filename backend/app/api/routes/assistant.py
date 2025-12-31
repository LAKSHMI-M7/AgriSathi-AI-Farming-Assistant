from fastapi import APIRouter, Body, Depends, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.openai_service import get_ai_response, generate_roadmap, client
from app.services.tts_service import generate_audio
from app.services import assistant_service
from app.db.database import get_db
import os
import uuid

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    language: str = "en"  # en, ml, hi
    user_id: int | None = None


@router.post("/query")
async def chat_with_ai(request: ChatRequest, db: Session = Depends(get_db)):
    response_text = await assistant_service.handle_query(request.message, request.language, request.user_id, db)
    audio_url = generate_audio(response_text, lang=request.language)
    return {"response": response_text, "audio_url": audio_url}


@router.post("/voice_query")
async def voice_chat(audio: UploadFile = File(...), language: str = "en", user_id: int | None = None, db: Session = Depends(get_db)):
    # Save audio temporarily
    temp_filename = f"temp_{uuid.uuid4()}.wav"
    temp_path = os.path.join("app", "static", "uploads", temp_filename)
    
    with open(temp_path, "wb") as buffer:
        buffer.write(await audio.read())
        
    try:
        # Transcribe
        with open(temp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        user_message = transcript.text
        response_text = await assistant_service.handle_query(user_message, language, user_id, db)
        audio_url = generate_audio(response_text, lang=language)
        
        return {
            "user_message": user_message,
            "response": response_text, 
            "audio_url": audio_url
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/roadmap")
def create_roadmap(goal: str = Body(..., embed=True), lang: str = "en"):
    roadmap = generate_roadmap(goal, lang)
    return {"roadmap": roadmap}
