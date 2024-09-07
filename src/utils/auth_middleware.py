from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from src.schemas.user_schema import UserResponse
from src.utils.jwt_utils import decode_access_token
from fastapi import HTTPException, status

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_paths: list[str] = None):
        super().__init__(app)
        self.exempt_paths = exempt_paths or []

    async def dispatch(self, request: Request, call_next):
        # Check if the request path is in the list of exempt paths
        if any(request.url.path.startswith(path) for path in self.exempt_paths):
            return await call_next(request)

        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token_type, token = auth_header.split()
            if token_type.lower() != "bearer":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"error": True, "message": "Invalid token type", "data": None},
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": True, "message": "Authorization header missing", "data": None},
            )

        try:
            # Decode the token and retrieve the user information
            user = decode_access_token(token)
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            # Attach the user information to the request state for use in route handlers
            user_response = UserResponse.model_validate(user)
            request.state.user = user_response
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": True, "message": str(e), "data": None},
            )

        # Proceed to the next middleware or route handler
        response = await call_next(request)
        return response
