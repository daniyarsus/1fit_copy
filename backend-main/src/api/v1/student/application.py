import os

from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.helper_functions.auth_handler import get_current_user
from src.helper_functions.word_replace_text import main_replace_text
from src.schemas.admin_notification import AdminNotificationCreate
from src.schemas.student_application import StudentApplicationCreate
from src.services.student import StudentService
from src.services.student_application import StudentApplicationService
from src.services.admin_notification import AdminNotificationService
from src.api.dependencies import student_application_service, admin_notification_service, student_service

student_application_router = APIRouter(prefix="/v1/student/application", tags=["student/application"])


@student_application_router.post(
    "/change/faculty/",
    status_code=200,
    summary="Заявление о смене факультета",
)
async def student_change_faculty_application(
        student_applications_service: Annotated[StudentApplicationService, Depends(student_application_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        admin_notifications_service: Annotated[AdminNotificationService, Depends(admin_notification_service)],
        user: Annotated[dict, Depends(get_current_user)],
        new_faculty: str
):
    try:
        student = await students_service.get_entity(user_id=user["id"])
    except Exception as e:
        raise HTTPException(status_code=404,
                            detail="Такого студента не существует, перезагрузите страницу и попробуйте еще раз")

    try:
        pattern_path = "media/applications/change_faculty.docx"
        result_path = f"media/user/{user['id']}/applications/change_faculty.docx"
        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        file_path = main_replace_text(
            pattern_path=pattern_path,
            result_path=result_path,
            texts={
                "ФИО": f"{student.firstname + ' ' + student.lastname}",
                "ФАКУЛЬТЕТ1": f"{student.faculty}",
                "ФАКУЛЬТЕТ2": f"{new_faculty}",
                "НОМЕРДОГОВОРА": f"{student.contract_number}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

    student_application_id = await student_applications_service.create_entity(
        StudentApplicationCreate(student_id=student.id, application_name="change_faculty", file_path=file_path)
    )

    if student_application_id:
        admin_notification_entity = AdminNotificationCreate(
            student_id=student.id,
            text="Студент оставил заявление на смену факультета",
            student_application_id=student_application_id,
            type="application"
        )
        await admin_notifications_service.create_entity(entity=admin_notification_entity)
        return student_application_id
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")



@student_application_router.post(
    "/change/university/",
    status_code=200,
    summary="Заявление о смене университета",
)
async def student_change_university_application(
        student_applications_service: Annotated[StudentApplicationService, Depends(student_application_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        admin_notifications_service: Annotated[AdminNotificationService, Depends(admin_notification_service)],
        user: Annotated[dict, Depends(get_current_user)],
        new_university: str
):
    try:
        student = await students_service.get_entity(user_id=user["id"])
        pattern_path = "media/applications/change_university.docx"
        result_path = f"media/user/{user['id']}/applications/change_university.docx"

        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        file_path = main_replace_text(
            pattern_path=pattern_path,
            result_path=result_path,
            texts={
                "ФИО": f"{student.firstname} {student.lastname}",
                "УНИВЕРСИТЕТ1": f"{student.university}",
                "УНИВЕРСИТЕТ2": f"{new_university}",
                "НОМЕРДОГОВОРА": f"{student.contract_number}"
            }
        )
        student_application_id = await student_applications_service.create_entity(
            StudentApplicationCreate(student_id=student.id, application_name="change_university", file_path=file_path)
        )
        if student_application_id:
            admin_notification_entity = AdminNotificationCreate(
                student_id=student.id,
                text="Студент оставил заявление на смену университета",
                student_application_id=student_application_id,
                type="application"
            )
            await admin_notifications_service.create_entity(entity=admin_notification_entity)
            return student_application_id
        else:
            raise HTTPException(status_code=400, detail="Не удалось создать объект")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")



@student_application_router.post(
    "/change/study_year/",
    status_code=200,
    summary="Заявление о смене факультета",
)
async def student_change_study_year_application(
        student_applications_service: Annotated[StudentApplicationService, Depends(student_application_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        admin_notifications_service: Annotated[AdminNotificationService, Depends(admin_notification_service)],
        user: Annotated[dict, Depends(get_current_user)],
        old_year: str,
        new_year: str
):
    try:
        try:
            student = await students_service.get_entity(user_id=user["id"])
        except Exception as e:
            raise HTTPException(status_code=404,
                                detail="Такого студента не существует, перезагрузите страницу и попробуйте еще раз")

        try:
            pattern_path = "media/applications/change_study_year.docx"
            result_path = f"media/user/{user['id']}/applications/change_study_year.docx"
            os.makedirs(os.path.dirname(result_path), exist_ok=True)
            file_path = main_replace_text(
                pattern_path=pattern_path,
                result_path=result_path,
                texts={
                    "ФИО": f"{student.firstname + ' ' + student.lastname}",
                    "ГОД1": f"{old_year}",
                    "ГОД2": f"{new_year}",
                    "НОМЕРДОГОВОРА": f"{student.contract_number}"
                }
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

        student_application_id = await student_applications_service.create_entity(
            StudentApplicationCreate(student_id=student.id, application_name="change_study_year", file_path=file_path)
        )

        if student_application_id:
            admin_notification_entity = AdminNotificationCreate(
                student_id=student.id,
                text="Студент оставил заявление на смену года обучения",
                student_application_id=student_application_id,
                type="application"
            )
            await admin_notifications_service.create_entity(entity=admin_notification_entity)
            return student_application_id
        else:
            raise HTTPException(status_code=400, detail="Не удалось создать объект")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")



@student_application_router.post(
    "/refund/",
    status_code=200,
    summary="Заявление о возврате",
)
async def student_refund_application(
        student_applications_service: Annotated[StudentApplicationService, Depends(student_application_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        admin_notifications_service: Annotated[AdminNotificationService, Depends(admin_notification_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    try:
        try:
            student = await students_service.get_entity(user_id=user["id"])
        except Exception as e:
            raise HTTPException(status_code=404,
                                detail="Такого студента не существует, перезагрузите страницу и попробуйте еще раз")

        try:
            pattern_path = "media/applications/refund.docx"
            result_path = f"media/user/{user['id']}/applications/refund.docx"
            os.makedirs(os.path.dirname(result_path), exist_ok=True)
            file_path = main_replace_text(
                pattern_path=pattern_path,
                result_path=result_path,
                texts={
                    "ФИО": f"{student.firstname + ' ' + student.lastname}",
                    "НОМЕРДОГОВОРА": f"{student.contract_number}",
                }
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

        student_application_id = await student_applications_service.create_entity(
            StudentApplicationCreate(student_id=student.id, application_name="refund", file_path=file_path)
        )

        if student_application_id:
            admin_notification_entity = AdminNotificationCreate(
                student_id=student.id,
                text="Студент оставил заявление на возврат",
                student_application_id=student_application_id,
                type="application",
            )
            await admin_notifications_service.create_entity(entity=admin_notification_entity)
            return student_application_id
        else:
            raise HTTPException(status_code=400, detail="Не удалось создать объект")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
