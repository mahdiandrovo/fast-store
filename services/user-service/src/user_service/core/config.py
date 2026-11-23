from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # JWT configuration
    JWT_PRIVATE_KEY_PATH: str = "secrets/private_key.pem"
    JWT_PUBLIC_KEY_PATH: str = "secrets/public_key.pem"
    JWT_ISSUER: str = "fast-store-user-service"
    JWT_AUDIENCE: str = "fast-store-api"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

settings = Settings()