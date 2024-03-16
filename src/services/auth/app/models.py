from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.services.auth.settings.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    phone: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[int] = mapped_column(default=1)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Определение отношения один к одному (one-to-one) с моделью EmailCode
    email_code = relationship("EmailCode", back_populates="user", uselist=False)

    # Определение отношения один к одному (one-to-one) с моделью PasswordCode
    password_code = relationship("PasswordCode", back_populates="user", uselist=False)


class EmailCode(Base):
    __tablename__ = "email_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(ForeignKey("users.email"))
    code: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Определение обратного отношения от EmailCode к User
    user = relationship("User", back_populates="email_code")


class PasswordCode(Base):
    __tablename__ = "password_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(ForeignKey("users.email"))
    code: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Определение обратного отношения от PasswordCode к User
    user = relationship("User", back_populates="password_code")