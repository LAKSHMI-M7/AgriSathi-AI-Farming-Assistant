from fastapi import APIRouter, UploadFile, File, Query
from app.services.openai_service import diagnose_leaf

router = APIRouter()

@router.post("/analyze")
async def analyze_leaf(file: UploadFile = File(...), lang: str = Query("en")):
    image_bytes = await file.read()
    
    # AI Diagnosis (Vision)
    diagnosis_raw = diagnose_leaf(image_bytes, lang)
    
    if not diagnosis_raw:
        # Fallback if AI fails
        return {
            "disease": "Unable to analyze",
            "health_score": 0,
            "suggestion": "Please ensure the photo is clear and try again.",
            "details": {}
        }

    # Parse structured output
    details = {}
    lines = diagnosis_raw.split('\n')
    for line in lines:
        if ":" in line:
            key, val = line.split(":", 1)
            details[key.strip().lower()] = val.strip()

    # Mapping keys for consistent frontend response
    # Expected keys: crop, disease, cure, cause, tip
    
    return {
        "crop": details.get("crop", "Unknown"),
        "disease": details.get("disease", "Healthy"),
        "cure": details.get("cure", "N/A"),
        "cause": details.get("cause", "N/A"),
        "tip": details.get("tip", "Keep monitoring."),
        "health_score": 100 if "healthy" in details.get("disease", "").lower() else 45,
        "raw": diagnosis_raw
    }
