from typing import Annotated

from pydantic import BaseModel, Field


class LogoutSchema(BaseModel):
    jwt: Annotated[str, Field(...)]
