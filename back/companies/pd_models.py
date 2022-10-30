from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCompany(BaseModel):
    id: int
    username: str | None
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None
    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    title: str | None
    description: str | None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    hidden: bool | None

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    hidden: bool

    class Config:
        orm_mode = True

