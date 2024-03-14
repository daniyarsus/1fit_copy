import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body, Form
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.schemas.check_student import CheckStudentCreate
from src.services.check import CheckService
from src.services.student import StudentService
from src.api.dependencies import check_student_service, student_service, check_service
from src.services.check_student import CheckStudentService

admin_check_student_router = APIRouter(prefix="/v1/admin/check-stud", tags=["admin/check/student"])



@admin_check_student_router.post(
    "/",
    status_code=201,
    summary="Добавление чека студента админом",
)
async def admin_student_check_create(
        check_students_service: Annotated[CheckStudentService, Depends(check_student_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        checks_service: Annotated[CheckService, Depends(check_service)],
        user: Annotated[dict, Depends(get_current_user)],
        student_id: int,
        check_id: int,
        price_usd: int,
        price_kzt: int,
        check_file: UploadFile
):
    print(student_id)
    student = await students_service.get_entity(id=student_id)
    print(student)
    if not student:
        raise HTTPException(status_code=404, detail="Такого студента не существует")
    check = await checks_service.get_entity(id=check_id)
    if not check:
        raise HTTPException(status_code=404, detail="Такого чека не существует")
    validate_user_admin(user["role_id"], [1])
    try:
        file_path = f"media/user/{student.user_id}/checks/"

        full_path = os.path.abspath(file_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        file_ext = mimetypes.guess_extension(check_file.content_type)
        check_file_path = os.path.join(full_path, f"{check.name}{file_ext}")

        with open(check_file_path, "wb") as f:  # Use 'wb' mode for writing binary data
            f.write(await check_file.read())  # Await reading of file content
        entity = CheckStudentCreate(student_id=student_id, check_id=check_id, price_usd=price_usd, price_kzt=price_kzt, check_file_path=check_file_path)
        check_student_id = await check_students_service.create_entity(entity=entity)
        if check_student_id:
            return check_student_id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось создать объект")



@admin_check_student_router.get(
    "/student/{id}/",
    status_code=200,
    summary="Получение чеков одного студента по его id",
)
async def admin_get_checks_student(
        id: int,
        check_students_service: Annotated[CheckStudentService, Depends(check_student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    check_students = await check_students_service.get_entities(student_id=id)
    if check_students:
        return check_students
    else:
        return []



@admin_check_student_router.get(
    "/",
    status_code=200,
    summary="Получение чеков всех студентов",
)
async def admin_get_document_of_students(
        check_students_service: Annotated[CheckStudentService, Depends(check_student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    checks_student = await check_students_service.get_entities()
    return checks_student


@admin_check_student_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление чека студента по id",
)
async def admin_delete_check_student(
        id: int,
        check_students_service: Annotated[CheckStudentService, Depends(check_student_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    document = await check_students_service.delete_entity(id=id)
    if document:
        return document
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")

