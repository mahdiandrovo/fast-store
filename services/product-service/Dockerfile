FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Product Service and its dependencies
RUN uv sync --frozen --no-dev --package product-service

# Document application port
EXPOSE 8002

# Start Product Service
CMD ["uv", "run", "--frozen", "--package", "product-service", "uvicorn", "product_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
