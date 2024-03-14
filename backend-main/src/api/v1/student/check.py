from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.helper_functions.auth_handler import get_current_user
from src.services.student import StudentService
from src.services.check_student import CheckStudentService
from src.api.dependencies import check_student_service, student_service

student_check_router = APIRouter(prefix="/v1/student/check", tags=["student/check"])


@student_check_router.get(
    "/",
    status_code=200,
    summary="Получение списка чеков студента",
)
async def student_get_checks(
        student_checks_service: Annotated[CheckStudentService, Depends(check_student_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    try:
        student = await students_service.get_entity(user_id=user["id"])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
                            detail="Такого студента не существует, перезагрузите страницу и попробуйте еще раз")
    student_checks = await student_checks_service.get_entities(student_id=student.id)
    if student_checks is None:
        return student_checks
    return student_checks