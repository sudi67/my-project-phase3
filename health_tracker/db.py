
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from health_tracker.models import Base


DATABASE_URL = "sqlite:///health_tracker.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    
    Base.metadata.create_all(bind=engine)
