# auth-microservice/src/schemas/role_schema.py

from pydantic import BaseModel

# Base schema for roles
class RoleBase(BaseModel):
    name: str

# Schema for creating a new role
class RoleCreate(RoleBase):
    pass

# Schema for returning role data in responses
class RoleResponse(RoleBase):
    id: int

    # Enables ORM mode to map SQLAlchemy models to Pydantic models
    class Config:
        orm_mode = True
