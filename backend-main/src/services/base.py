from src.reposotories.repository import AbstractRepository
from pydantic import BaseModel


class BaseService:
    def __init__(self, base_repo: AbstractRepository):
        self.base_repo: AbstractRepository = base_repo

    async def create_entity(self, entity):
        if isinstance(entity, BaseModel):
            entity = entity.model_dump()
        entity_id = await self.base_repo.add_one(data=entity)
        return entity_id

    async def get_entity(self, **filters):
        entity = await self.base_repo.get_one(**filters)
        return entity

    async def get_entities(self, **filters):
        entities = await self.base_repo.get_all(**filters)
        return entities

    async def update_entity(self, entity, **filters):
        if isinstance(entity, BaseModel):
            entity = entity.model_dump()
        updated_entity = await self.base_repo.edit_one(**filters, data=entity)
        return updated_entity

    async def delete_entity(self, **filters):
        return await self.base_repo.delete_one(**filters)
