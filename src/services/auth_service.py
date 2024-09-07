from datetime import timedelta
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user_model import User
from src.schemas.user_schema import UserCreate, UserResponse
from src.utils.hash_utils import get_password_hash
from src.models.response_model import ResponseModel
from src.utils.jwt_utils import create_access_token
from src.utils.common import get_user_by_email

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, user_create: UserCreate, db: AsyncSession) -> ResponseModel:
        """
        Register a new user.

        Args:
            user_create (UserCreate): The user data to create a new user.
            db (AsyncSession): The database session.

        Returns:
            ResponseModel: The response model containing the new user data.
        
        Raises:
            ValueError: If the user is already registered.
        """
        # Check if user already exists
        result = db.execute(select(User).filter_by(email=user_create.email))
        existing_user = result.scalars().first()

        if existing_user:
            raise ValueError("User already registered")

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create a new user
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )

        # Add and commit the new user
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user_response = UserResponse.model_validate(new_user)
        return ResponseModel(error=False, message="User registered successfully", data=user_response.model_dump())

    
    async def authenticate_user(self, email: str, password: str, db: AsyncSession) -> ResponseModel:
        """
        Authenticate a user based on email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            db (AsyncSession): The database session.

        Returns:
            ResponseModel: A response model with authentication status and data.
        """
        try:
            result = await get_user_by_email(email=email, db=db)
            user = result.scalars().first()

            if user and self.pwd_context.verify(password, user.hashed_password):
                access_token_expires = timedelta(minutes=60)
                access_token = create_access_token(
                    data={"id": user.id, "username": user.username,"email": user.email}, expires_delta=access_token_expires
                )
                return ResponseModel(
                    error=False,
                    message="Login successful",
                    data={"access_token": access_token, "token_type": "bearer"}
                )
            else:
                raise Exception("Invalid credentials")
        except Exception as e:
            return ResponseModel(
                error=True,
                message=str(e),
                data=None
            )
        

    async def get_user_by_id(self, userId: int, db: AsyncSession) -> ResponseModel:
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