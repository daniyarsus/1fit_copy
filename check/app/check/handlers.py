from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from check.app.check import schemas
from check.app.utils.dependencies.db import get_session
from check.app.check.controllers import ItemController


router = APIRouter()


@router.post(
    "/create-item"
)
async def create_item_endpoint(
        item: schemas.CreateItem,
        db: AsyncSession = Depends(get_session)
):
    item_controller = ItemController(
        db=db
    )
    return await item_controller.create_item(
        item=item
    )
