from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.part import PartService
from src.schemas.part import PartCreate
from src.api.dependencies import part_service

admin_part_router = APIRouter(prefix="/v1/admin/part", tags=["admin/part"])


@admin_part_router.get(
    "/",
    status_code=200,
    summary="Получение списка частей Документов страны",
)
async def admin_get_parts(
        parts_service: Annotated[PartService, Depends(part_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    parts = await parts_service.get_entities()
    return parts


@admin_part_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение части Документа страны",
)
async def admin_get_part(
        id: int,
        parts_service: Annotated[PartService, Depends(part_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    part = await parts_service.get_entity(id=id)
    return part


@admin_part_router.post(
    "/",
    status_code=201,
    summary="Добавление части Документа страны",
)
async def admin_create_part(
        part: PartCreate,
        parts_service: Annotated[PartService, Depends(part_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    part = await parts_service.create_entity(part)
    if part:
        return part
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")


@admin_part_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление этапа по id",
)
async def admin_delete_part(
        id: int,
        parts_service: Annotated[PartService, Depends(part_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    part = await parts_service.delete_entity(id=id)
    if part:
        return part
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")