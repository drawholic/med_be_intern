from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Union


class UserCompany(BaseModel):
    id: int
    username: Union[str, None]
    email: EmailStr
    created_at: datetime
    updated_at: Union[datetime, None]

    class Config:
        orm_mode = True


class CompanyBase(BaseModel):
    title: Union[str, None]
    description: Union[str, None]

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    hidden: Union[bool, None]

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None]
    hidden: bool

    class Config:
        orm_mode = True
class Request(BaseModel):
    id: int
    user_id: int
    company_id: int
    updated_at: Union[datetime, None]
    created_at: datetime
    user: UserCompany

    class Config:
        orm_mode = True


