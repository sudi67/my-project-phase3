# health_tracker/db.py
# Setup SQLAlchemy engine and session for the Health Simplified CLI Application

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from health_tracker.models import Base

# Using SQLite for simplicity; can be changed to PostgreSQL by changing the URL
DATABASE_URL = "sqlite:///health_tracker.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
