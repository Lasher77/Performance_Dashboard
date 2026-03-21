from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://steuerpilot:changeme@postgres:5432/steuerpilot"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = "changeme-generate-a-real-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30
    JWT_REFRESH_EXPIRATION_DAYS: int = 7
    UPLOAD_DIR: str = "/app/uploads"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
