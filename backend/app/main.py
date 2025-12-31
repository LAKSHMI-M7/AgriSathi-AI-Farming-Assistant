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
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(farmer.router, prefix="/farmer", tags=["Farmer"])
app.include_router(assistant.router, prefix="/assistant", tags=["AI Assistant"])
app.include_router(weather.router, prefix="/weather", tags=["Weather"])
app.include_router(schemes.router, prefix="/government", tags=["Schemes"])
app.include_router(recommend.router, prefix="/cultivation", tags=["Cultivation"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(doctor.router, prefix="/doctor", tags=["Doctor"])

@app.get("/")
def read_root():
    return {"message": "AgriSathi API is running"}
