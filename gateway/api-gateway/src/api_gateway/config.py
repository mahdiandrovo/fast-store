import os


USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://localhost:8001"
)

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://localhost:8002"
)

JWT_PUBLIC_KEY_PATH = os.getenv(
    "JWT_PUBLIC_KEY_PATH",
    "secrets/public_key.pem"
)

JWT_ISSUER = os.getenv(
    "JWT_ISSUER",
    "fast-store-user-service"
)

JWT_AUDIENCE = os.getenv(
    "JWT_AUDIENCE",
    "fast-store-api"
)