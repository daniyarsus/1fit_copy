from sqlalchemy.orm import Mapped, mapped_column

from app.settings.db.connection import Base

from app.schemas.user import ReadUserModel


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[int] = mapped_column(unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> ReadUserModel:
        return ReadUserModel(
            id=User.id,
            username=self.username,
            password=self.password,
            email=self.email,
            phone=self.phone,
            is_verified=self.is_verified
        )
