import os

from pydantic_settings import BaseSettings

from pydantic import Field


class Settings(BaseSettings):
    DB_USER: str = Field(..., env='DB_USER')
    DB_PASS: str = Field(..., env='DB_PASS')
    DB_HOST: str = Field(..., env='DB_HOST')
    DB_PORT: str = Field(..., env='DB_PORT')
    DB_NAME: str = Field(..., env='DB_NAME')

    JWT_SECRET_KEY: str = Field(..., env='JWT_SECRET_KEY')
    ALGORITHM: str = Field(..., env='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(..., env='REFRESH_TOKEN_EXPIRE_DAYS')

    REDIS_URL: str = Field(..., env='REDIS_URL')

    SMTP_DOMAIN_NAME: str = Field(..., env='SMTP_DOMAIN_NAME')
    SMTP_PORT: int = Field(..., env='SMTP_PORT')
    SMTP_API_KEY: str = Field(..., env='SMTP_API_KEY')
    SMTP_EMAIL_FROM: str = Field(..., env='SMTP_EMAIL_FROM')

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".env")


settings = Settings()


print(settings.DB_PASS)
