import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_FILE = "backend/agrisathi.db"

# Vercel's serverless functions are read-only except for the /tmp directory
if os.environ.get("VERCEL") or os.environ.get("VERCEL_URL"):
    DB_FILE = "/tmp/agrisathi.db"
    if not os.path.exists(DB_FILE) and os.path.exists("backend/agrisathi.db"):
        try:
            shutil.copy("backend/agrisathi.db", DB_FILE)
        except Exception:
            pass

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
