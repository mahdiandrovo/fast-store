from contextlib import asynccontextmanager

from fastapi import FastAPI

from product_service.api.v1.products import router as products_router
from product_service.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Fast Store - Product Service",
    description="Product catalog management microservice",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(products_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "service": "product-service",
        "status": "running",
        "message": "Welcome to Fast Store Product Service",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}