from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.user_model import User
from src.schemas.user_schema import UserCreate
from src.utils.hash_utils import get_password_hash, verify_password

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, user_create: UserCreate, db: AsyncSession) -> User:
        """
        Register a new user.

        Args:
            user_create (UserCreate): The user data to create a new user.
            db (AsyncSession): The database session.

        Returns:
            User: The newly created user.
        
        Raises:
            ValueError: If the user is already registered.
        """
        async with db() as session:
            result = await session.execute(select(User).filter_by(email=user_create.email))
            existing_user = result.scalar_one_or_none()
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

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    async def authenticate_user(self, email: str, password: str, db: AsyncSession) -> Optional[User]:
        """
        Authenticate a user based on email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.
            db (AsyncSession): The database session.

        Returns:
            Optional[User]: The user if authentication is successful, otherwise None.
        """
        async with db() as session:
            result = await session.execute(select(User).filter_by(email=email))
            user = result.scalar_one_or_none()

            if user and self.pwd_context.verify(password, user.hashed_password):
                return user
            return None

    async def get_user_by_email(self, email: str, db: AsyncSession) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            email (str): The user's email.
            db (AsyncSession): The database session.

        Returns:
            Optional[User]: The user if found, otherwise None.
        """
        async with db() as session:
            result = await session.execute(select(User).filter_by(email=email))
            user = result.scalar_one_or_none()
            return user
