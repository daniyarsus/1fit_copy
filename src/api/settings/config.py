import os

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class PostgresDataBaseSettings:
    POSTGRES_DATABASE_URL = os.environ.get("POSTGRES_DATABASE_URL")


@dataclass
class Settings:
    def __init__(self):
        self.pg_database = PostgresDataBaseSettings()


settings: Settings = Settings()
