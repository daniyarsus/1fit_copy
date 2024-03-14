from fastapi import APIRouter, Depends
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.student_application import StudentApplicationService
from src.api.dependencies import student_application_service

admin_student_application_router = APIRouter(prefix="/v1/admin/student/application", tags=["admin/student/application"])


@admin_student_application_router.get(
    "/all/",
    status_code=200,
    summary="Получение списка заявлении",
)
async def admin_get_student_applications(
        student_applications_service: Annotated[StudentApplicationService, Depends(student_application_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    student_applications = await student_applications_service.get_entities()
    return student_applications