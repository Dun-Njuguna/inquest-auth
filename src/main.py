from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from src.utils.app_lifespan import lifespan
from src.utils.exception_handlers import global_exception_handler, global_http_exception_handler, validation_exception_handler
from src.controllers.auth_controller import router as auth_router
from src.controllers import auth_controller, user_controller

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, global_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# Register the routers
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(user_controller.router, prefix="/users", tags=["users"])

# Root endpoint, useful for health checks
@app.get("/")
def read_root():
    return {"message": "Welcome to the Auth Microservice"}


# Entry point for running the app directly
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
