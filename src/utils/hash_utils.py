# auth-microservice/src/utils/hash_utils.py

from passlib.context import CryptContext

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verify a plain password against a hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Hash a password for storage
def get_password_hash(password):
    return pwd_context.hash(password)
