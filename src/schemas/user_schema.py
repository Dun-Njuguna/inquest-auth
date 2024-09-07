from pydantic import BaseModel, EmailStr

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for returning user data in responses
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    # Enables ORM mode to map SQLAlchemy models to Pydantic models
    class Config:
        from_attributes = True

# Schema for returning an authentication token
class Token(BaseModel):
    access_token: str
    token_type: str
