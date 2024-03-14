from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.city import CityService
from src.schemas.city import CityCreate
from src.api.dependencies import city_service

admin_city_router = APIRouter(prefix="/v1/admin/city", tags=["admin/city"])


@admin_city_router.get(
    "/",
    status_code=200,
    summary="Получение списка городов",
)
async def admin_get_cities(
        cities_service: Annotated[CityService, Depends(city_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    cities = await cities_service.get_entities()
    return cities


@admin_city_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение города",
)
async def admin_get_city(
        id: int,
        cities_service: Annotated[CityService, Depends(city_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    city = await cities_service.get_entity(id=id)
    if city:
        return city
    else:
         raise HTTPException(status_code=404, detail="Не удалось найти объект")



@admin_city_router.post(
    "/",
    status_code=201,
    summary="Добавление города",
)
async def admin_create_city(
        city: CityCreate,
        cities_service: Annotated[CityService, Depends(city_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    city = await cities_service.create_entity(city)
    if city:
        return city
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")


@admin_city_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление города по id",
)
async def admin_delete_city(
        id: int,
        cities_service: Annotated[CityService, Depends(city_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    city = await cities_service.delete_entity(id=id)
    if city:
        return city
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")