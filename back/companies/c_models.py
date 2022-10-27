from pydantic import BaseModel
from datetime import datetime

class CompanyBase(BaseModel):
    title: str
    description: str


class CompanyCreate(CompanyBase):
    owner: int


class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    hidden: bool
    owner: int

    class Config:
        orm_mode = True

