import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.student import StudentService
from src.schemas.student import AdminStudentUpdate, AdminStudentCreateInput, AdminStudentCreate
from src.api.dependencies import student_service, user_service
from src.services.user import UserService

admin_student_router = APIRouter(prefix="/v1/admin/student", tags=["admin/student"])


@admin_student_router.post(
    "/",
    status_code=201,
    summary="Создание админом студента"
)
async def admin_create_student(
        users_service: Annotated[UserService, Depends(user_service)],
        user: Annotated[dict, Depends(get_current_user)],
        students_service: Annotated[StudentService, Depends(student_service)],
        student: AdminStudentCreateInput
):
    validate_user_admin(user["role_id"], [1])
    user_id = await users_service.create_entity({"email": student.email, "password": student.password, "role_id": 2})
    if user_id:
        student_id = await students_service.create_entity(AdminStudentCreate(user_id=user_id, **student.dict()))
        if student_id:
            return student_id
        else:
            raise HTTPException(status_code=400, detail="Student not created")
    else:
        raise HTTPException(status_code=400, detail="User not created")


@admin_student_router.get(
    "/",
    status_code=200,
    summary="Получение списка студентов",
)
async def admin_get_students(
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)],
        country_id: int = None,
        status_id: int = None
):
    validate_user_admin(user["role_id"], [1])
    if country_id is not None:
        students = await students_service.get_entities(study_country_id=country_id)
    elif status_id is not None:
        student = await students_service.get_entity(status_id=status_id)
        students = [student] if student else []
    else:
        students = await students_service.get_entities()
    if not students:
        return []
    filtered_students = [student for student in students if getattr(student, "status_id", None) not in [3, 5]]

    return filtered_students

@admin_student_router.get(
    "/archive/",
    status_code=200,
    summary="Получение списка студентов",
)
async def admin_get_archive_students(
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    students = await students_service.get_entities()
    return students



@admin_student_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение студента по id",
)
async def admin_get_student(
        id: int,
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    student = await students_service.get_entity(id=id)
    if student:
        return student
    else:
        raise HTTPException(status_code=400, detail="Невозможно получить объект")


@admin_student_router.put(
    "/{id}/",
    status_code=200,
    summary="Изменение студента по id",
)
async def admin_edit_student(
        id: int,
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)],
        entity: AdminStudentUpdate
):
    validate_user_admin(user["role_id"], [1])
    student = await students_service.update_entity(entity=entity, id=id)
    if student:
        return True
    else:
        raise HTTPException(status_code=400, detail="Невозможно изменить объект")


@admin_student_router.delete(
    "/{id}/",
    status_code=200,
    summary="Изменение студента по id",
)
async def admin_delete_student(
        id: int,
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    student = await students_service.delete_entity(id=id)
    if student:
        return student
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")


@admin_student_router.patch(
    "/{id}/photo/",
    status_code=200,
    summary="Изменение/Добавление фотки студента по его id"
)
async def admin_patch_student_image(
        id: int,
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)],
        photo: UploadFile = File(...),
):
    validate_user_admin(user["role_id"], [1])
    student_id = await students_service.get_entity(id=id)
    if not student_id:
        raise HTTPException(status_code=404, detail="Студент не найден")
    try:
        file_path = f"media/user/{user['id']}/"

        full_path = os.path.abspath(file_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        photo_ext = mimetypes.guess_extension(photo.content_type)
        photo_path = os.path.join(full_path, f"photo{photo_ext}")

        with open(photo_path, "wb") as f:
            f.write(await photo.read())

        student = await students_service.update_entity({"photo_path": photo_path}, user_id=user["id"])
        return student
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))