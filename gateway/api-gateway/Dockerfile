
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install API Gateway and its dependencies
RUN uv sync --frozen --no-dev --package api-gateway

# Document application port
EXPOSE 8000

# Start API Gateway
CMD ["uv", "run", "--frozen", "--package", "api-gateway", "uvicorn", "api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]