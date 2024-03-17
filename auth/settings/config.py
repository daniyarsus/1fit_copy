import os

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class PostgresDatabaseConfig:
    DB_HOST = os.environ.get("DB_HOST2")
    DB_PORT = os.environ.get("DB_PORT2")
    DB_NAME = os.environ.get("DB_NAME2")
    DB_USER = os.environ.get("DB_USER2")
    DB_PASS = os.environ.get("DB_PASS2")

    def __str__(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class JWTConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")


@dataclass
class Settings:
    def __init__(self):
        self.pg_database = PostgresDatabaseConfig()
        self.jwt_config = JWTConfig()


settings: Settings = Settings()

print(str(settings.pg_database))
