from app.repository.base import SQLAlchemyRepository, RedisRepository

from app.models.user import User


class UserRepository(SQLAlchemyRepository):
    model = User
