import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from typing import Annotated
from src.helper_functions.auth_handler import get_current_user
from src.schemas.admin_notification import AdminNotificationCreate
from src.services.admin_notification import AdminNotificationService
from src.services.student import StudentService
from src.services.document import DocumentService
from src.services.part import PartService
from src.services.document_student import DocumentStudentService
from src.schemas.document_student import DocumentStudentCreate
from src.api.dependencies import student_service, document_service, document_student_service, part_service, \
    admin_notification_service

student_document_router = APIRouter(prefix="/v1/student/document", tags=["student/document"])


@student_document_router.get(
    "/part/{part_id}/",
    status_code=200,
    summary="Получение всех документов студента с информацией о файлах и correct",
)
async def student_document_get(
        students_service: Annotated[StudentService, Depends(student_service)],
        documents_service: Annotated[DocumentService, Depends(document_service)],
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        user: Annotated[dict, Depends(get_current_user)],
        part_id: int
):
    student = await students_service.get_entity(user_id=user["id"])
    if not student:
        raise HTTPException(status_code=404, detail="Объект не найден")

    # Получаем объекты Document
    documents = await documents_service.get_entities(part_id=part_id)
    if not documents:
        return []

    # Получаем все записи DocumentStudent для данного студента
    student_documents = await document_students_service.get_entities(student_id=student.id)

    # Создаем словарь для хранения информации о каждом документе
    document_info = {doc.id: {"file_path": None, "correct": None} for doc in documents}

    # Заполняем словарь информацией о файлах и correct для документов, которые есть в DocumentStudent
    for student_document in student_documents:
        if student_document.document.id in document_info:
            document_info[student_document.document.id]["file_path"] = student_document.file_path
            document_info[student_document.document.id]["correct"] = student_document.correct

    # Формируем результирующий список документов с правильными file_path и correct
    result_documents = []
    for doc in documents:
        doc_info = document_info[doc.id]
        result_documents.append({
            "id": doc.id,
            "name": doc.name,
            "file_path": doc_info["file_path"],
            "correct": doc_info["correct"]
        })

    return result_documents


@student_document_router.get(
    "/parts/",
    status_code=200,
    summary="Получение всех партов студента с информацией о файлах",
)
async def student_part_get_with_files(
        students_service: Annotated[StudentService, Depends(student_service)],
        parts_service: Annotated[PartService, Depends(part_service)],
        documents_service: Annotated[DocumentService, Depends(document_service)],
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    student = await students_service.get_entity(user_id=user["id"])
    student_documents = await document_students_service.get_entities(student_id=student.id)
    parts = await parts_service.get_entities(country_id=student.study_country_id)

    result_parts = []
    for part in parts:
        part_info = part.dict()  # Получаем информацию о части
        documents = await documents_service.get_entities(part_id=part.id)
        if documents is None:
            return []

        # Создаем словарь для хранения file_path и correct каждого документа
        document_info = {doc.id: {"file_path": None, "correct": None} for doc in documents}

        # Заполняем словарь file_path и correct для документов, которые есть в DocumentStudent
        for student_document in student_documents:
            if student_document.document.id in document_info:
                document_info[student_document.document.id]["file_path"] = student_document.file_path
                document_info[student_document.document.id]["correct"] = student_document.correct

        # Формируем результирующий список документов с правильными file_path и correct
        result_documents = []
        for doc in documents:
            doc_info = document_info[doc.id]
            result_documents.append({
                "id": doc.id,
                "name": doc.name,
                "file_path": doc_info["file_path"],
                "correct": doc_info["correct"]
            })

        part_info["documents"] = result_documents  # Добавляем информацию о документах к части
        result_parts.append(part_info)

    return result_parts



@student_document_router.post(
    "/",
    status_code=201,
    summary="Добавление документов студента",
)
async def student_document_create(
        students_service: Annotated[StudentService, Depends(student_service)],
        documents_service: Annotated[DocumentService, Depends(document_service)],
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        admin_notifications_service: Annotated[AdminNotificationService, Depends(admin_notification_service)],
        user: Annotated[dict, Depends(get_current_user)],
        document_id: int,
        file: UploadFile
):
    student = await students_service.get_entity(user_id=user["id"])
    student_documents_to_delete = await document_students_service.get_entities(student_id=student.id, document_id=document_id)
    if student_documents_to_delete is not None:
        for stud_doc in student_documents_to_delete:
            await document_students_service.delete_entity(id=stud_doc.id)
    document = await documents_service.get_entity(id=document_id)

    try:
        file_path = f"media/user/{user['id']}/documents/"

        full_path = os.path.abspath(file_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        file_ext = mimetypes.guess_extension(file.content_type)
        photo_path = os.path.join(full_path, f"{document.name}{file_ext}")

        with open(photo_path, "wb") as f:
            f.write(await file.read())

        student_document_id = await document_students_service.create_entity(DocumentStudentCreate(student_id=student.id, document_id=document_id, file_path=photo_path))
        if student_document_id:
            admin_notification_entity = (AdminNotificationCreate(student_id=student.id, text="Студент заполнил новый документ",
                                                                 document_student_id=student_document_id, type="document"))
            await admin_notifications_service.create_entity(entity=admin_notification_entity)
            return student_document_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
