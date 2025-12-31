from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.models.all_models import User
from app.schemas import UserResponse

router = APIRouter()

class ProfileUpdateRequest(BaseModel):
    user_id: int
    full_name: str
    village: str
    state: str
    primary_crop: str

@router.get("/profile", response_model=UserResponse)
def get_farmer_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return user

@router.get("/stats/{user_id}")
def get_farmer_stats(user_id: int, db: Session = Depends(get_db)):
    from app.models.all_models import Document
    doc_count = db.query(Document).filter(Document.user_id == user_id).count()
    # Mock chat count for now as we don't have a chat table yet
    return {
        "chat_count": 12, 
        "advice_count": doc_count,
        "primary_crop": db.query(User.primary_crop).filter(User.id == user_id).scalar() or "Paddy"
    }

@router.post("/update")
def update_farmer_profile(request: ProfileUpdateRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    user.full_name = request.full_name
    user.village = request.village
    user.state = request.state
    user.primary_crop = request.primary_crop
    
    db.commit()
    db.refresh(user)
    return {"status": "success", "user": user}

@router.get("/{user_id}", response_model=UserResponse)
def get_farmer_details_legacy(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return user
