from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
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
