from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.admin_notification import AdminNotificationService
from src.api.dependencies import admin_notification_service

admin_notification_router = APIRouter(prefix="/v1/admin/notification", tags=["admin/notification"])


@admin_notification_router.get(
    "/",
    status_code=200,
    summary="Получение списка уведомлении",
)
async def admin_get_notifications(
        admin_notifications_service: Annotated[AdminNotificationService, Depends(admin_notification_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    admin_notifications = await admin_notifications_service.get_entities()
    return admin_notifications


@admin_notification_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение уведомления через id",
)
async def admin_get_notification(
        id: int,
        admin_notifications_service: Annotated[AdminNotificationService, Depends(admin_notification_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    await admin_notifications_service.update_entity(id=id, entity={'checked': True})
    admin_notification = await admin_notifications_service.get_entity(id=id)
    if admin_notification:
        return admin_notification
    else:
        raise HTTPException(status_code=404, detail="Не удалось найти объект")







