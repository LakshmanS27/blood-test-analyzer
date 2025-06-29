from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# 👉 SQLite URL: use this for dev
DATABASE_URL = "sqlite:///./reports.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Run this once at app startup
def init_db():
    Base.metadata.create_all(bind=engine)
