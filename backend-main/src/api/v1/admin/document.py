from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.api.validator import validate_user_admin
from src.helper_functions.auth_handler import get_current_user
from src.services.document import DocumentService
from src.schemas.document import DocumentCreate
from src.api.dependencies import document_service

admin_document_router = APIRouter(prefix="/v1/admin/document", tags=["admin/document"])


@admin_document_router.get(
    "/",
    status_code=200,
    summary="Получение списка документов",
)
async def admin_get_documents(
        documents_service: Annotated[DocumentService, Depends(document_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    documents = await documents_service.get_entities()
    return documents


@admin_document_router.post(
    "/",
    status_code=201,
    summary="Создание документа"
)
async def admin_create_document(
        documents_service: Annotated[DocumentService, Depends(document_service)],
        user: Annotated[dict, Depends(get_current_user)],
        entity: DocumentCreate
):
    validate_user_admin(user["role_id"], [1])
    document = await documents_service.create_entity(entity=entity)
    if document:
        return document
    else:
        raise HTTPException(status_code=400, detail="Не удалось создать объект")


@admin_document_router.get(
    "/{id}/",
    status_code=200,
    summary="Получение документа по id",
)
async def admin_get_document(
        id: int,
        documents_service: Annotated[DocumentService, Depends(document_service)],
        user: Annotated[dict, Depends(get_current_user)]
):
    validate_user_admin(user["role_id"], [1])
    document = await documents_service.get_entity(id=id)
    if document:
        return document
    else:
        raise HTTPException(status_code=400, detail="Невозможно получить объект")


@admin_document_router.put(
    "/{id}/",
    status_code=200,
    summary="Изменение документа по id",
)
async def admin_edit_document(
        id: int,
        documents_service: Annotated[DocumentService, Depends(document_service)],
        user: Annotated[dict, Depends(get_current_user)],
        entity: DocumentCreate
):
    validate_user_admin(user["role_id"], [1])
    document = await documents_service.update_entity(entity=entity, id=id)
    if document:
        return document
    else:
        raise HTTPException(status_code=400, detail="Невозможно изменить объект")


@admin_document_router.delete(
    "/{id}/",
    status_code=200,
    summary="Удаление документа по id",
)
async def admin_delete_document(
        id: int,
        documents_service: Annotated[DocumentService, Depends(document_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    validate_user_admin(user["role_id"], [1])
    document = await documents_service.delete_entity(id=id)
    if document:
        return document
    else:
        raise HTTPException(status_code=400, detail="Невозможно удалить объект")
