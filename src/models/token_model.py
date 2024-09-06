# auth-microservice/src/models/token_model.py

from sqlalchemy import Column, Integer, String
from src.models.base import Base

# SQLAlchemy model for the Token table
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True)
    user_id = Column(Integer)
