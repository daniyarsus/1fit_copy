from src.helper_functions.auth_handler import bcrypt_context
from src.services.base import BaseService


class UserService(BaseService):
    async def create_entity(self, entity):
        hashed_password = bcrypt_context.hash(entity["password"])
        lowered_email = entity["email"].lower()
        entity.pop("password")
        entity["hashed_password"] = hashed_password
        entity["email"] = lowered_email
        entity_id = await self.base_repo.add_one(data=entity)
        return entity_id

