from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
from api_gateway.routes.users import router as users_router
from api_gateway.routes.products import router as products_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0)
    )

    yield

    await app.state.http_client.aclose()

app = FastAPI(
    title="Fast Store API Gateway",
    description="Central entry point for Fast Store microservices",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["User Service"],
)

app.include_router(
    products_router,
    prefix="/api/v1/products",
    tags=["Product Service"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Fast Store API Gateway"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway"
    }