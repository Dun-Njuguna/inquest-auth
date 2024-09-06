# src/controllers/auth_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.user_schema import UserCreate, UserResponse, Token
from src.services.auth_service import AuthService
from src.utils.jwt_utils import create_access_token
from datetime import timedelta

router = APIRouter()

auth_service = AuthService()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    # Register a new user
    return await auth_service.register_user(user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate the user and return a token
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
