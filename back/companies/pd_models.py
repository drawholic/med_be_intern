from pydantic import BaseModel
from datetime import datetime


class UserCompany(BaseModel):
    id: int
    username: str | None
    created_at: datetime
    updated_at: datetime | None
    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    title: str
    description: str


class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    hidden: bool
    owner_id: int
    owner: UserCompany

    class Config:
        orm_mode = True

