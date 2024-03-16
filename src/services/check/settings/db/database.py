from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.services.auth.settings.config import settings

async_engine = create_async_engine(
    url=str(settings.pg_database),
    #url="sqlite+aiosqlite:///./test.db",
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
