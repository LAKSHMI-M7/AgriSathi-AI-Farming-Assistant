import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get absolute path to the backend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
DB_FILE_PATH = os.path.join(backend_dir, "agrisathi.db")
# SQLAlchemy expects triple slash for absolute paths on Windows or root relative
DB_FILE = f"/{DB_FILE_PATH.replace(':', '|')}" if os.name == 'nt' else f"/{DB_FILE_PATH}"

# Vercel's serverless functions are read-only except for the /tmp directory
if os.environ.get("VERCEL") or os.environ.get("VERCEL_URL"):
    DB_FILE = "/tmp/agrisathi.db"
    if not os.path.exists(DB_FILE) and os.path.exists(os.path.join(backend_dir, "agrisathi.db")):
        try:
            shutil.copy(os.path.join(backend_dir, "agrisathi.db"), DB_FILE)
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
