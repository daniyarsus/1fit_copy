from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.check import CheckService
from src.schemas.check import CheckCreate
from src.api.dependencies import check_service

admin_check_router = APIRouter(prefix="/v1/admin/check", tags=["admin/check"])


@admin_check_router.get(
    "/",
    status_code=200,
    summary="Получение списка чеков страны",
)
async def admin_get_checks(
        checks_service: Annotated[CheckService, Depends(check_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    checks = await checks_service.get_entities()
    return checks


@admin_check_router.get(
    "/country/{id}/",
    status_code=200,
    summary="Получение чеков страны по id страны",
)
async def admin_get_check_by_country(
        id: int,
        checks_service: Annotated[CheckService, Depends(check_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    check = await checks_service.get_entities(country_id=id)
    return check


@admin_check_router.post(
    "/",
    status_code=201,
    summary="Добавление чека для страны",
)
async def admin_create_check(
        check: CheckCreate,
        checks_service: Annotated[CheckService, Depends(check_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    check = await checks_service.create_entity(check)
    if check:
        return check
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")


@admin_check_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление чека по id",
)
async def admin_delete_check(
        id: int,
        checks_service: Annotated[CheckService, Depends(check_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    check = await checks_service.delete_entity(id=id)
    if check:
        return check
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")


