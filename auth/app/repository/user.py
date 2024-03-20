from app.repository.base import SQLAlchemyRepository

from app.models.user import User


class UserRepository(SQLAlchemyRepository):
    model = User
