import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .db.database import engine, Base
from .api.routes import auth, farmer, assistant, weather, schemes, recommend, documents, doctor

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgriSathi", description="AI Farming Assistant")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mounting Static for Uploads
STATIC_DIR = "backend/app/static" if (os.environ.get("VERCEL") or os.environ.get("VERCEL_URL")) else "app/static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(farmer.router, prefix="/api/farmer", tags=["Farmer"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["AI Assistant"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(schemes.router, prefix="/api/government", tags=["Schemes"])
app.include_router(recommend.router, prefix="/api/cultivation", tags=["Cultivation"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(doctor.router, prefix="/api/doctor", tags=["Doctor"])

@app.get("/")
def read_root():
    return {"message": "AgriSathi API is running"}
