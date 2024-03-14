from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.university import UniversityService
from src.schemas.university import UniversityCreate
from src.api.dependencies import university_service

admin_university_router = APIRouter(prefix="/v1/admin/university", tags=["admin/university"])


@admin_university_router.get(
    "/",
    status_code=200,
    summary="Получение списка университетов",
)
async def admin_get_universities(
        universities_service: Annotated[UniversityService, Depends(university_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    universities = await universities_service.get_entities()
    return universities


@admin_university_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение университета",
)
async def admin_get_university(
        id: int,
        universities_service: Annotated[UniversityService, Depends(university_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    university = await universities_service.get_entity(id=id)
    if university:
        return university
    else:
        raise HTTPException(status_code=404, detail="Не удалось найти объект")


@admin_university_router.post(
    "/",
    status_code=201,
    summary="Добавление университета",
)
async def admin_create_university(
        university: UniversityCreate,
        universities_service: Annotated[UniversityService, Depends(university_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    university = await universities_service.create_entity(university)
    if university:
        return university
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")


@admin_university_router.get(
    "/city/{id}/",
    status_code=200,
    summary="Получение университетов города",
)
async def admin_get_city_universities(
        id: int,
        universities_service: Annotated[UniversityService, Depends(university_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    universities = await universities_service.get_entities(city_id=id)
    return universities



@admin_university_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление университета по id",
)
async def admin_delete_city(
        id: int,
        universities_service: Annotated[UniversityService, Depends(university_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    university = await universities_service.delete_entity(id=id)
    if university:
        return university
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")

