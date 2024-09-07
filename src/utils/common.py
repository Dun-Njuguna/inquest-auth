from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from src.models.response_model import ResponseModel
from src.schemas.user_schema import UserResponse
from src.models.user_model import User

async def get_user_by_email(email: str, db: AsyncSession) -> Optional[User]:
    """
    Retrieve a user by email.

    Args:
        email (str): The user's email.
        db (AsyncSession): The database session.

    Returns:
        Optional[User]: The user if found, otherwise None.
    """

    try:
        user = db.execute(select(User).filter_by(email=email))
        if user is None:
            raise ValueError("Query result is None")
        
        return user
    except ValueError as e:
        # Log and raise value errors
        raise e
    except Exception as e:
        # Log unexpected errors
        raise RuntimeError("An unexpected error occurred.")

async def get_user_by_id( userId: int, db: AsyncSession) -> ResponseModel:
    try:
        query = select(User).where(User.id == userId)
        result = db.execute(query)
        user = result.scalars().first()
        
        if user :
            user_response = UserResponse.model_validate(user)
            return ResponseModel(
                error=False,
                message="Request successful",
                data= user_response.model_dump()
            )
        else:
            raise Exception("Invalid user id")
    except Exception as e:
        return ResponseModel(
            error=True,
            message=str(e),
            data=None
        )