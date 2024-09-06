# auth-microservice/src/models/user_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base

# SQLAlchemy model for the User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Relationship with Role model
    roles = relationship("Role", back_populates="users")
