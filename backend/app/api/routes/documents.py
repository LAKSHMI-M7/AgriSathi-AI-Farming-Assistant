from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from typing import List
import shutil
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.all_models import Document, User
from app.schemas import DocumentResponse

router = APIRouter()
UPLOAD_DIR = "app/static/uploads"

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    # Save file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Save to DB
    new_doc = Document(
        filename=file.filename,
        file_path=f"/static/uploads/{file.filename}",
        category=category,
        user_id=user_id,
        upload_date=datetime.utcnow()
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

@router.get("/list/{user_id}", response_model=List[DocumentResponse])
def list_documents(user_id: int, db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.user_id == user_id).all()
    return docs

@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        # Check if file exists and remove
        if os.path.exists(doc.file_path.lstrip("/")): # remove leading / if using relative
            # Actually path is stored as /static/uploads/...
            # We need to map it back to app/static/uploads/...
            real_path = os.path.join("app", doc.file_path.lstrip("/")) 
            if os.path.exists(real_path):
                os.remove(real_path)
                
        db.delete(doc)
        db.commit()
        return {"status": "deleted"}
    return {"status": "not found"}
