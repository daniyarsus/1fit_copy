import os
from dataclasses import dataclass
from pydantic_settings import BaseSettings
from pydantic import Field


class EnvSettings(BaseSettings):
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
    SMTP_PORT: str = Field(..., env='SMTP_PORT')
    SMTP_API_KEY: str = Field(..., env='SMTP_API_KEY')
    SMTP_EMAIL_FROM: str = Field(..., env='SMTP_EMAIL_FROM')

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")


env_settings = EnvSettings()


@dataclass
class PostgresDatabaseConfig:
    DB_USER: str = env_settings.DB_USER
    DB_PASS: str = env_settings.DB_PASS
    DB_HOST: str = env_settings.DB_HOST
    DB_PORT: str = env_settings.DB_PORT
    DB_NAME: str = env_settings.DB_NAME

    def __str__(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class JWTConfig:
    SECRET_KEY: str = env_settings.JWT_SECRET_KEY
    ALGORITHM: str = env_settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS: int = env_settings.REFRESH_TOKEN_EXPIRE_DAYS


@dataclass
class RedisConfig:
    REDIS_URL: str = env_settings.REDIS_URL


@dataclass
class SMTPConfig:
    DOMAIN_NAME: str = env_settings.SMTP_DOMAIN_NAME
    SMTP_PORT: str = env_settings.SMTP_PORT
    API_KEY: str = env_settings.SMTP_API_KEY
    EMAIL_FROM: str = env_settings.SMTP_EMAIL_FROM


@dataclass
class Settings:
    def __init__(self):
        self.pg_database = PostgresDatabaseConfig()
        self.jwt_config = JWTConfig()
        self.regis_config = RedisConfig()
        self.smtp_config = SMTPConfig()


settings: Settings = Settings()
