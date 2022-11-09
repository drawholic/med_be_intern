from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Union

class BaseAdmin(BaseModel):
    id: int
    email: EmailStr
    username: Union[str, None]
    created_at: datetime
    updated_at: Union[datetime, None]

    class Config:
        orm_mode = True


class Admin(BaseModel):
    user: BaseAdmin

    class Config:
        orm_mode = True