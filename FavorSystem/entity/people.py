from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel, DateTime

class People(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, )
    name: str
    birthday: date = Field(default=None)
    gendar: int
    favor: float = 0.0
