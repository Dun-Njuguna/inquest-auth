from pydantic import BaseModel

# Schema for access token
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for parsing token data (used for token validation)
class TokenData(BaseModel):
    username: str | None = None
