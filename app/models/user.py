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

    @classmethod
    def delete_unverified_users(cls, session):
        """
        Удаляет всех пользователей, которые не подтвердили свою учетную запись в течение 7 дней.
        """
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        unverified_users = session.query(cls).filter(cls.is_verified == False,
                                                     cls.created_at <= seven_days_ago).all()
        for user in unverified_users:
            session.delete(user)
        session.commit()

    def to_read_model(self) -> ReadUserModel:
        """
        Преобразует объект пользователя в ReadUserMode
        """
        return ReadUserModel(
            id=self.id,
            username=self.username,
            password=self.password,
            email=self.email,
            phone=self.phone,
            is_verified=self.is_verified
        )
