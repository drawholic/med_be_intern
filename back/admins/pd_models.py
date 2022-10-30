from pydantic import BaseModel, EmailStr
from datetime import datetime


class BaseAdmin(BaseModel):
    id: int
    email: EmailStr
    username: str | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class Admin(BaseModel):
    user: BaseAdmin
    class Config:
        orm_mode = True