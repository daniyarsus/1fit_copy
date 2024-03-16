from fastapi import APIRouter

from src.services.check.app.check import schemas
from src.services.check.app.utils.dependencies.db import get_session
from src.services.check.app.check.controllers import ItemController


router = APIRouter()


@router.post(
    "/create-item"
)
async def create_item_endpoint(
        item: schemas.CreateItem,
        db: Session = Depends(get_session)
):
    item_controller = ItemController(
        db=db
    )
    return await item_controller.create_item(
        item=item
    )
