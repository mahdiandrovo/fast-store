from fastapi import FastAPI

from inventory_service.api.v1.inventory import router as inventory_router


app = FastAPI(
    title="Fast Store - Inventory Service",
    description="Inventory management microservice",
    version="0.1.0",
)

app.include_router(
    inventory_router,
    prefix="/api/v1/inventory",
    tags=["Inventory"],
)

@app.get("/")
async def root():
    return {
        "service": "inventory-service",
        "status": "running",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}