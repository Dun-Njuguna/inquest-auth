from fastapi import APIRouter, Request, HTTPException, Depends, status
from src.models.response_model import ResponseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.env.database import get_db
from src.utils.common import get_user_by_id

router = APIRouter()

@router.get("/me", response_model=ResponseModel)
async def read_users_me(request: Request):
    user_data = request.state.user.dict()
    user_data.pop('exp', None)  # Remove 'exp' field
    response = ResponseModel(
        error=False,
        message="Request successful",
        data=user_data
    )
    return response

@router.get("/{user_id}", response_model=ResponseModel)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
