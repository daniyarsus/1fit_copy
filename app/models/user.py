from datetime import datetime

from sqlalchemy import BigInteger, Column
from sqlalchemy.orm import Mapped, mapped_column

from app.settings.db.connection import Base

from app.schemas.user import ReadUserModel


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    #phone: Mapped[int] = mapped_column(unique=True)
    phone = Column(BigInteger)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_read_model(self) -> ReadUserModel:
        return ReadUserModel(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email,
            phone=self.phone,
            is_verified=self.is_verified
        )
