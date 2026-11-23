
from contextlib import asynccontextmanager

from fastapi import FastAPI

from user_service.api.v1.users import router as users_router
from user_service.db.session import engine

from user_service.api.v1.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await engine.dispose()

app = FastAPI(
    title="Fast Store - User Service",
    description="User management and authentication microservice",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(
    users_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

@app.get("/")
async def root():
    return {
        "service": "user-service",
        "status": "running",
        "message": "Welcome to Fast Store",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}