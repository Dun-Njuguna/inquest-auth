# src/main.py

from fastapi import FastAPI
from src.controllers.auth_controller import router as auth_router
from src.controllers import auth_controller, user_controller
from src.migrations import run_migrations

app = FastAPI()

# Register the routers
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
app.include_router(user_controller.router, prefix="/users", tags=["users"])

# Root endpoint, useful for health checks
@app.get("/")
def read_root():
    return {"message": "Welcome to the Auth Microservice"}

# Run migrations on startup
@app.on_event("startup")
async def on_startup():
    run_migrations()

# Entry point for running the app directly
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
