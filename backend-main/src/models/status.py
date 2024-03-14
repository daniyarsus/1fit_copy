from sqlalchemy import String, Integer, Column
from settings.database.database_connection import Base
from src.schemas.status import StatusRead


class Status(Base):
    __tablename__ = "Status"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def to_read_model(self) -> StatusRead:
        return StatusRead(
            id=self.id,
            name=self.name
        )
