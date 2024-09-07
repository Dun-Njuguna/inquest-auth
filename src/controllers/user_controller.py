from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.env.database import get_db
from src.models.response_model import ResponseModel
from src.schemas.user_schema import UserResponse
from src.services.auth_service import AuthService
from src.utils.jwt_utils import get_current_user

router = APIRouter()

auth_service = AuthService()

@router.get("/me", response_model=ResponseModel)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    user_data = current_user
    user_data.pop('exp', None)
    # Create the response using the modified user data
    response = ResponseModel(
                error=False,
                message="Request successful",
                data=user_data
            )
    return response

@router.get("/{user_id}", response_model=ResponseModel)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # Get a specific user's details
    user = await auth_service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
