import os


USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://localhost:8001"
)

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://localhost:8002"
)