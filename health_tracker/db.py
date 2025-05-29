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
