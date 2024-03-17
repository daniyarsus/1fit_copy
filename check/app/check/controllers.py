from abc import abstractmethod, ABC

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from check.app import models
from check.app.check import schemas


class BaseItemController(ABC):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def create_item(self, item: schemas.CreateItem):
        pass


class ItemController(BaseItemController):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create_item(self, item: schemas.CreateItem):
        try:
            item = models.Check(
                name=item.name
            )

            self.db.add(item)
            await self.db.commit()

            return JSONResponse(
                status_code=201,
                content={
                    "message": "Item created successfully"
                }
            )

        except HTTPException as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
