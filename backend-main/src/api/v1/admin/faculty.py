from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.schemas.faculty import FacultyCreate
from src.services.faculty import FacultyService
from src.api.dependencies import faculty_service

admin_faculty_router = APIRouter(prefix="/v1/admin/facuty", tags=["admin/faculty"])



@admin_faculty_router.get(
    "/",
    status_code=200,
    summary="Получение списка факультетов",
)
async def admin_get_faculties(
        faculties_service: Annotated[FacultyService, Depends(faculty_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    faculties = await faculties_service.get_entities()
    return faculties


@admin_faculty_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение факультета",
)
async def admin_get_faculty(
        id: int,
        faculties_service: Annotated[FacultyService, Depends(faculty_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    faculty = await faculties_service.get_entity(id=id)
    if faculty:
        return faculty
    else:
        raise HTTPException(status_code=404, detail="Не удалось найти объект")


@admin_faculty_router.post(
    "/",
    status_code=201,
    summary="Добавление факультета",
)
async def admin_create_faculty(
        faculty: FacultyCreate,
        faculties_service: Annotated[FacultyService, Depends(faculty_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    faculty = await faculties_service.create_entity(faculty)
    if faculty:
        return faculty
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")


@admin_faculty_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление факультета по id",
)
async def admin_delete_faculty(
        id: int,
        faculties_service: Annotated[FacultyService, Depends(faculty_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    faculty = await faculties_service.delete_entity(id=id)
    if faculty:
        return faculty
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")
