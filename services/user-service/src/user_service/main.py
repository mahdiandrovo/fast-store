from fastapi import FastAPI

app = FastAPI(
    title = "Fast Store - User Service",
    description = "User management and authentication microservice",
    version = "0.1.0"
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
    return {
        "status": "healthy",
    }