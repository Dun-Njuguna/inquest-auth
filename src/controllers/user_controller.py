# src/controllers/user_controller.py

from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user_schema import UserResponse
from src.services.auth_service import AuthService
from src.utils.jwt_utils import get_current_user

router = APIRouter()

auth_service = AuthService()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    # Get the current logged-in user's details
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    # Get a specific user's details
    user = await auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
