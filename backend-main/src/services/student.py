from src.services.base import BaseService


class StudentService(BaseService):
    async def get_entity(self, **filters):
        entity = await self.base_repo.get_one(**filters)
        if entity:
            return entity.to_read_model()



