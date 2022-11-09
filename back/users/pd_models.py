from pydantic import BaseModel, validator, EmailStr
from .exceptions import PasswordMismatchException
from fastapi import HTTPException
from datetime import datetime
from typing import Union
class UserBase(BaseModel):
    email: EmailStr    


class UserUpgrade(BaseModel):

    username: Union[str, None] = None
    password1: Union[str, None] = None
    password2: Union[str, None] = None

    @validator('password2', allow_reuse=True)
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise PasswordMismatchException
        return v


class UserSignInPass(UserBase):
    password: str


class UserSignUp(UserBase):
    password1: str
    password2: str
    
    @validator('password2', allow_reuse=True)
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise HTTPException(status_code=400, detail='passwords dont match')
        return v


class User(UserBase):
    id: int
    username: Union[str, None]
    created_at: datetime
    updated_at: Union[datetime, None]

    class Config:
        orm_mode = True


class UserAuth(User):
    token: str



