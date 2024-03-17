from sqlalchemy.orm import Mapped, mapped_column

from check.settings.db.database import Base


class Check(Base):
    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
