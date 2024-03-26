from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.settings.config import settings


DB_USER = settings.pg_database.DB_USER
DB_PASS = settings.pg_database.DB_PASS
DB_HOST = settings.pg_database.DB_HOST
DB_PORT = settings.pg_database.DB_PORT
DB_NAME = settings.pg_database.DB_NAME


DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async_engine = create_async_engine(
    url=DB_URL,
    #url="sqlite+aiosqlite:///./auth.db",
    echo=False
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    @property
    def pk(self):
        """Возвращает первичный ключ объектов"""
        return getattr(self, self.__mapper__.primary_key[0].name)

    def __repr__(self):
        return f'<{self.__class__.__name__}(id={self.pk})>'
