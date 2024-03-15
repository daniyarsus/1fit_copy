from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from api.services.v1.auth_service.db import async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
