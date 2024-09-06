from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.env.config import settings
from src.schemas.user_schema import UserResponse
from src.services.auth_service import AuthService

# OAuth2PasswordBearer is used to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create an access token for a user
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token for a user.

    Args:
        data (dict): Data to encode in the token.
        expires_delta (Optional[timedelta]): Token expiration time.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Decode an access token to retrieve the username
def decode_access_token(token: str) -> Optional[str]:
    """
    Decode an access token to retrieve the username.

    Args:
        token (str): The JWT token to decode.

    Returns:
        Optional[str]: The username if the token is valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# Get the current user based on the token
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Retrieve the current user from the JWT token.

    Args:
        token (str): The JWT token from the Authorization header.

    Returns:
        UserResponse: The user details if the token is valid.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    auth_service = AuthService()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        email = decode_access_token(token)
        if email is None:
            raise credentials_exception
        user = auth_service.get_user_by_email(email)  # Make sure this method exists in your AuthService
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
