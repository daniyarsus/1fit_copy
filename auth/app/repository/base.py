from abc import ABC, abstractmethod

from redis import asyncio as redis

from sqlalchemy import insert, select, delete, update

from app.settings.db.connection import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, filters):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, id):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_all(self, **filters):
        async with async_session() as session:
            stmt = select(self.model)
            if filters:
                stmt = stmt.filter_by(**filters)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def get_one(self, **filters):
        async with async_session() as session:
            stmt = select(self.model).filter_by(**filters)
            res = await session.execute(stmt)
            entity = res.scalar_one_or_none()
            if entity:
                return entity

    async def delete_one(self, **filters):
        async with async_session() as session:
            stmt = delete(self.model).filter_by(**filters)
            result = await session.execute(stmt)
            await session.commit()
            return bool(result.rowcount)

    async def edit_one(self, data, **filters):
        async with async_session() as session:
            stmt = update(self.model).filter_by(**filters).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()


class AbstractRedisRepository(ABC):
    @abstractmethod
    async def set_value(self, key: str, value: str, expire: int = None):
        pass

    @abstractmethod
    async def get_value(self, key: str):
        pass

    @abstractmethod
    async def delete_key(self, key: str):
        pass


class RedisRepository(AbstractRedisRepository):
    def __init__(self, redis_url: str):
        self._redis = redis.from_url(redis_url)

    async def set_value(self, key: str, value: str, expire: int = None):
        await self._redis.set(name=key, value=value, ex=expire)

    async def get_value(self, key: str):
        return await self._redis.get(key=key)

    async def delete_key(self, key: str):
        await self._redis.delete(key=key)
