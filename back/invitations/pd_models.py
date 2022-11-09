from pydantic import BaseModel
from datetime import datetime
from typing import List, Union


class Company(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: Union[datetime, None]
    hidden: bool

    class Config:
        orm_model = True


class Invitation(BaseModel):
    company: Company

    class Config:
        orm_mode = True