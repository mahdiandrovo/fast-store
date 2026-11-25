
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Inventory Service and its dependencies
RUN uv sync --frozen --no-dev --package inventory-service

# Document application port
EXPOSE 8003

# Start Inventory Service
CMD ["uv", "run", "--frozen", "--package", "inventory-service", "uvicorn", "inventory_service.main:app", "--host", "0.0.0.0", "--port", "8003"]