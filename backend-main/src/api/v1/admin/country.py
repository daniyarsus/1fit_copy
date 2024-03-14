from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.country import CountryService
from src.schemas.country import CountryCreate
from src.api.dependencies import country_service

admin_country_router = APIRouter(prefix="/v1/admin/country", tags=["admin/country"])


@admin_country_router.get(
    "/",
    status_code=200,
    summary="Получение списка стран",
)
async def admin_get_countries(
        countries_service: Annotated[CountryService, Depends(country_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    countries = await countries_service.get_entities()
    return countries


@admin_country_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение страны",
)
async def admin_get_country(
        id: int,
        countries_service: Annotated[CountryService, Depends(country_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    country = await countries_service.get_entity(id=id)
    if country:
        return country
    else:
        raise HTTPException(status_code=404, detail="Не удалось найти объект")


@admin_country_router.post(
    "/",
    status_code=201,
    summary="Добавление страны",
)
async def admin_create_country(
        country: CountryCreate,
        countries_service: Annotated[CountryService, Depends(country_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    country = await countries_service.create_entity(country)
    if country:
        return country
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")



@admin_country_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление страны по id",
)
async def admin_delete_country(
        id: int,
        countries_service: Annotated[CountryService, Depends(country_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    country = await countries_service.delete_entity(id=id)
    if country:
        return country
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")




