FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install User Service and its dependencies
RUN uv sync --frozen --no-dev --package user-service

# Document application port
EXPOSE 8001

# Start User Service
CMD ["uv", "run", "--frozen", "--package", "user-service", "uvicorn", "user_service.main:app", "--host", "0.0.0.0", "--port", "8001"]