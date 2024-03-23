import os

from typing import Optional

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class PostgresDatabaseConfig:
    DB_HOST = os.environ.get("DB_HOST_AUTH")
    DB_PORT = os.environ.get("DB_PORT_AUTH")
    DB_NAME = os.environ.get("DB_NAME_AUTH")
    DB_USER = os.environ.get("DB_USER_AUTH")
    DB_PASS = os.environ.get("DB_PASS_AUTH")

    def __str__(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@dataclass
class JWTConfig:
    SECRET_KEY = str(os.environ.get("SECRET_KEY"))
    ALGORITHM = str(os.environ.get("ALGORITHM"))
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS"))

    def __str__(self):
        return (
            f"SECRET_KEY: {self.SECRET_KEY},"
            f"ALGORITHM: {self.ALGORITHM}, "
            f"ACCESS_TOKEN_EXPIRE_MINUTES: {self.ACCESS_TOKEN_EXPIRE_MINUTES}, "
            f"REFRESH_TOKEN_EXPIRE_DAYS: {self.REFRESH_TOKEN_EXPIRE_DAYS}"
        )


@dataclass
class RegisConfig:
    REDIS_URL_AUTH = str(os.environ.get("REDIS_URL_AUTH"))

    def __str__(self):
        return (
            f"REDIS_URL_AUTH: {self.REDIS_URL_AUTH}"
        )


@dataclass
class SMTPConfig:
    DOMAIN_NAME = str(os.environ.get("SMTP_DOMAIN_NAME"))
    SMTP_PORT = str(os.environ.get("SMTP_PORT"))
    API_KEY = str(os.environ.get("SMTP_API_KEY"))
    EMAIL_FROM = str(os.environ.get("SMTP_EMAIL_FROM"))

    def __str__(self):
        return (
            f"DOMAIN_NAME: {self.DOMAIN_NAME}, "
            f"SMTP_PORT: {self.SMTP_PORT}, "
            f"API_KEY: {self.API_KEY}, "
            f"EMAIL_FROM: {self.EMAIL_FROM}"
        )


@dataclass
class Settings:
    def __init__(self):
        self.pg_database = PostgresDatabaseConfig()
        self.jwt_config = JWTConfig()
        self.regis_config = RegisConfig()
        self.smtp_config = SMTPConfig()


settings: Settings = Settings()
