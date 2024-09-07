from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.login_model import LoginModel
from src.models.response_model import ResponseModel
from src.env.database import get_db
from src.schemas.user_schema import UserCreate
from src.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/register", response_model=ResponseModel)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await auth_service.register_user(user, db)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=ResponseModel)
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    content_type = request.headers.get('Content-Type', '')

    try:
        if 'application/json' in content_type:
            json_data = await request.json()
            form_data = LoginModel(**json_data)
        elif 'application/x-www-form-urlencoded' in content_type:
            form_data = await request.form()
            form_data = LoginModel(email=form_data['email'], password=form_data['password'])
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported content type"
            )

        response = await auth_service.authenticate_user(form_data.email, form_data.password, db)
        
        if response.error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=response.message
            )

        return response

    except ValidationError as e:
        raise RequestValidationError(e.errors())
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)