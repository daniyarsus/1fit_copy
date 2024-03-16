from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.check.app.check import schemas
from src.services.check.app.utils.dependencies.db import get_session
from src.services.check.app.check.controllers import ItemController


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
