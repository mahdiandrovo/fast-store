from fastapi import Depends, FastAPI, Request
from contextlib import asynccontextmanager
import httpx
from api_gateway.routes.users import router as users_router
from api_gateway.routes.products import router as products_router
from api_gateway.routes.auth import router as auth_router
from api_gateway.dependencies import authenticate_request
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("api_gateway")

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
    dependencies=[Depends(authenticate_request)],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    logger.info(
        "Incoming request: %s %s",
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    logger.info(
        "Response: %s %s - Status: %s",
        request.method,
        request.url.path,
        response.status_code,
    )

    return response

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

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
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