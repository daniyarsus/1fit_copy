import mimetypes
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.schemas.document_student import DocumentStudentCreate
from src.schemas.student_notification import StudentNotificationCreate
from src.services.document import DocumentService
from src.services.document_student import DocumentStudentService
from src.services.student_notification import StudentNotificationService
from src.api.dependencies import document_student_service, student_service, document_service, student_notification_service
from src.services.student import StudentService

from src.api.dependencies import part_service
from src.services.part import PartService

admin_document_student_router = APIRouter(prefix="/v1/admin/doc-stud", tags=["admin/document/student"])



@admin_document_student_router.post(
    "/",
    status_code=201,
    summary="Добавление документов студента админом",
)
async def admin_student_document_create(
        students_service: Annotated[StudentService, Depends(student_service)],
        documents_service: Annotated[DocumentService, Depends(document_service)],
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        user: Annotated[dict, Depends(get_current_user)],
        document_id: int,
        student_id: int,
        file: UploadFile
):
    validate_user_admin(user["role_id"], [1])
    student = await students_service.get_entity(id=student_id)
    document = await documents_service.get_entity(id=document_id)
    student_documents_to_delete = await document_students_service.get_entities(student_id=student.id, document_id=document_id)
    if student_documents_to_delete is not None:
        for stud_doc in student_documents_to_delete:
            await document_students_service.delete_entity(id=stud_doc.id)
    try:
        file_path = f"media/user/{student.user_id}/documents/"

        full_path = os.path.abspath(file_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        file_ext = mimetypes.guess_extension(file.content_type)
        photo_path = os.path.join(full_path, f"{document.name}{file_ext}")

        with open(photo_path, "wb") as f:  # Use 'wb' mode for writing binary data
            f.write(await file.read())  # Await reading of file content

        student_document_id = await document_students_service.create_entity(DocumentStudentCreate(student_id=student.id, document_id=document_id, file_path=photo_path))
        if student_document_id:
            return student_document_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@admin_document_student_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение документа студента по id",
)
async def admin_get_document_student_a(
        id: int,
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    document = await document_students_service.get_entity(id=id)
    print(document)
    return document



@admin_document_student_router.get(
    "/student/{id}/",
    status_code=200,
    summary="Получение документа студента по id студента",
)
async def admin_get_document_of_student(
        id: int,
        students_service: Annotated[StudentService, Depends(student_service)],
        documents_service: Annotated[DocumentService, Depends(document_service)],
        parts_service: Annotated[PartService, Depends(part_service)],
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    student = await students_service.get_entity(id=id)
    if not student:
        raise HTTPException(status_code=404, detail="Объект не найден")
    parts = await parts_service.get_entities(country_id=student.study_country_id)
    part_ids = [part.id for part in parts]
    result = []
    for part_id in part_ids:
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

        result.append({"part_id": part_id, "documents": result_documents})
    return result

@admin_document_student_router.get(
    "/",
    status_code=200,
    summary="Получение документов всех студентов",
)
async def admin_get_document_of_students(
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        students_service: Annotated[StudentService, Depends(student_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    document_students = await document_students_service.get_entities()

    if document_students:
        formatted_data = []
        for document_student in document_students:
            student_id = document_student.student.id
            student = await students_service.get_entity(id=student_id)
            document_info = {
                "student_id": student_id,
                "fullname": student.firstname + " " + student.lastname,
                "documents": [{
                    "stud_doc_id": document_student.id,
                    "name": document_student.document.name,
                    "document_id": document_student.document.id,
                    "file_path": document_student.file_path,
                    "correct": document_student.correct
                }]
            }
            student_found = False
            for item in formatted_data:
                if item["student_id"] == student_id:
                    item["documents"].append(document_info["documents"][0])
                    student_found = True
                    break
            if not student_found:
                formatted_data.append(document_info)
        return formatted_data
    else:
        return []


@admin_document_student_router.delete(
    "/{id}/",
    status_code=200,
    summary="Изменение документа студента по id",
)
async def admin_delete_document_student(
        id: int,
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    document = await document_students_service.delete_entity(id=id)
    if document:
        return document
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")



@admin_document_student_router.patch(
    "/{id}/correct/",
    status_code=200,
    summary="У студента документ будет высвечиваться как правильный и придет уведомление",
)
async def admin_correct_document_student(
        id: int,
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        student_notifications_service: Annotated[StudentNotificationService, Depends(student_notification_service)],
        user: Annotated[dict, Depends(get_current_user)],
        text_for_student: str = Body("Правильно заполнен документ")
):
    validate_user_admin(user["role_id"], [1])
    student_document = await document_students_service.update_entity({"correct": True}, id=id)
    if student_document:
        await student_notifications_service.create_entity(entity=StudentNotificationCreate(student_id=student_document.student_id, text=text_for_student))
        return True
    else:
        raise HTTPException(status_code=400, detail="Невозможно изменить объект")



@admin_document_student_router.patch(
    "/{id}/incorrect/",
    status_code=200,
    summary="У студента документ будет высвечиваться как неправильный и придет уведомление",
)
async def admin_incorrect_document_student(
        id: int,
        document_students_service: Annotated[DocumentStudentService, Depends(document_student_service)],
        student_notifications_service: Annotated[StudentNotificationService, Depends(student_notification_service)],
        user: Annotated[dict, Depends(get_current_user)],
        text_for_student: str = Body("Неправильно заполнен документ")
):
    validate_user_admin(user["role_id"], [1])
    student_document = await document_students_service.update_entity({"correct": False}, id=id)
    if student_document:
        await student_notifications_service.create_entity(entity=StudentNotificationCreate(student_id=student_document.student_id, text=text_for_student))
        return True
    else:
        raise HTTPException(status_code=400, detail="Невозможно изменить объект")