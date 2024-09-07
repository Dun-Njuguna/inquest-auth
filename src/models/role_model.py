from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base


# SQLAlchemy model for the Role table
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # ForeignKey to associate role with a specific user
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship with User model
    users = relationship("User", back_populates="roles")
