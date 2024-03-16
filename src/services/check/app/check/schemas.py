from typing import Optional

from pydantic import BaseModel


class BaseItem(BaseModel):
    class Config:
        from_attributes = True


class CreateItem(BaseItem):
    name: Optional[str]
