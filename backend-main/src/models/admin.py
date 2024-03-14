from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from settings.database.database_connection import Base
from src.schemas.admin import AdminRead


class Admin(Base):
    __tablename__ = "Admin"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('User.id'), nullable=False)
    role = Column(String, nullable=False)
    user = relationship('User')
    def to_read_model(self) -> AdminRead:
        return AdminRead(
            id=self.id,
            user_id=self.user_id,
            role=self.role,
            email=self.user.email,
        )