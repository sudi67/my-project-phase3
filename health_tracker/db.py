<<<<<<< HEAD
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
=======
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

try:
    import psycopg2
except ImportError:
    psycopg2 = None

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')

if psycopg2 is None:
    # Fallback to SQLite if psycopg2 is not installed
    DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
>>>>>>> e08c1f3 (Add database connection setup and comprehensive CRUD tests for models)
