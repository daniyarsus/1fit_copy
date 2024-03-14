from fastapi import APIRouter, Depends
from typing import Annotated
from src.helper_functions.auth_handler import get_current_user
from src.services.student import StudentService
from src.services.student_notification import StudentNotificationService
from src.api.dependencies import student_notification_service, student_service

student_notification_router = APIRouter(prefix="/v1/student/notification", tags=["student/notification"])


@student_notification_router.get(
    "/",
    status_code=200,
    summary="Получение списка уведомлении",
)
async def student_get_notifications(
        student_notifications_service: Annotated[StudentNotificationService, Depends(student_notification_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    student = await students_service.get_entity(user_id=user["id"])
    student_notifications = await student_notifications_service.get_entities(student_id=student.id)
    return student_notifications


# @student_notification_router.get(
#     "/{id}/",
#     status_code=200,
#     summary="Получение уведомления через id",
# )
# async def student_get_notification(
#         id: int,
#         student_notifications_service: Annotated[StudentNotificationService, Depends(student_notification_service)],
#         user: Annotated[dict, Depends(get_current_user)]
# ):
#     await student_notifications_service.update_entity(id=id, entity={'checked': True})
#     student_notification = await student_notifications_service.get_entity(id=id)
#     if student_notification:
#         return student_notification
#     else:
#         raise HTTPException(status_code=404, detail="Не удалось найти объект")







