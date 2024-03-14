import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Annotated
from src.helper_functions.auth_handler import get_current_user
from src.services.student import StudentService
from src.schemas.student import StudentCreateInput
from src.api.dependencies import student_service

student_student_router = APIRouter(prefix="/v1/student", tags=["student"])


@student_student_router.get(
    "/me/",
    status_code=200,
    summary="Получение данных студента",
)
async def student_get_me(
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    students = await students_service.get_entity(user_id=user["id"])
    return students


@student_student_router.put(
    "/me/",
    status_code=200,
    summary="Обновление данных студента",
)
async def student_update_me(
        student: StudentCreateInput,
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    student_id = await students_service.get_entity(user_id=user["id"])
    if not student_id:
        raise HTTPException(status_code=404, detail="Студент не найден")
    await students_service.update_entity(student, user_id=user["id"])
    return student_id


@student_student_router.patch(
    "/me/photo/",
    status_code=200,
    summary="Обновление/Создание фотки студента",
)
async def student_patch_me_photo(
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)],
        photo: UploadFile = File(...)
):
    student_id = await students_service.get_entity(user_id=user["id"])
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


@student_student_router.get(
    "/me/photo/",
    status_code=200,
    summary="Брать фотки студента",
)
async def student_patch_me_photo(
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    student = await students_service.get_entity(user_id=user["id"])
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return student.photo_path


@student_student_router.patch(
    "/me/passport/",
    status_code=200,
    summary="Обновление/Создание паспорта студента",
)
async def student_patch_me_passport(
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)],
        passport: UploadFile = File(...)
):
    student_id = await students_service.get_entity(user_id=user["id"])
    if not student_id:
        raise HTTPException(status_code=404, detail="Студент не найден")
    try:
        file_path = f"media/user/{user['id']}/"

        full_path = os.path.abspath(file_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        passport_photo_ext = mimetypes.guess_extension(passport.content_type)
        passport_photo = os.path.join(full_path, f"passport{passport_photo_ext}")

        with open(passport_photo, "wb") as f:
            f.write(await passport.read())

        student = await students_service.update_entity({"passport_photo": passport_photo}, user_id=user["id"])
        return student
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))