from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.env.config import settings

# SQLAlchemy engine setup
engine = create_engine(settings.DATABASE_URL)

# Session local class to use in your DB interaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
