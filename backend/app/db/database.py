import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get absolute path to the backend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
DB_PATH = os.path.join(backend_dir, "agrisathi.db")

# Vercel's serverless functions are read-only except for the /tmp directory
if os.environ.get("VERCEL") or os.environ.get("VERCEL_URL"):
    tmp_db = "/tmp/agrisathi.db"
    if not os.path.exists(tmp_db) and os.path.exists(DB_PATH):
        try:
            shutil.copy(DB_PATH, tmp_db)
        except Exception:
            pass
    DB_PATH = tmp_db

# Standardize path for SQLite URI (especially for Windows)
db_uri_path = DB_PATH.replace("\\", "/")
# For absolute paths, we need 4 slashes total: sqlite:////C:/path/to/db
if not db_uri_path.startswith("/"):
    db_uri_path = f"/{db_uri_path}"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_uri_path}"

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
