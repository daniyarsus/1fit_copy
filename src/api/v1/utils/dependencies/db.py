from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.db.database import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
