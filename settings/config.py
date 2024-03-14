import os

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class PostgresDataBaseSettings:
    POSTGRES_DATABASE_URL = os.environ.get("POSTGRES_DATABASE_URL")


@dataclass
class PostgresDatabaseConfig:
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")

    def __str__(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class Settings:
    def __init__(self):
        self.pg_database = PostgresDatabaseConfig()


settings: Settings = Settings()

