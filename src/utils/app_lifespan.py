from fastapi import FastAPI
from typing import AsyncIterator
from src.utils.migrations import run_migrations

async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # No migration code here
    await run_migrations()
    yield
