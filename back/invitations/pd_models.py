from pydantic import BaseModel
from datetime import datetime

class Company(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime | None
    hidden: bool

    class Config:
        orm_model = True


class Invitation(BaseModel):
    company: Company

    class Config:
        orm_mode = True