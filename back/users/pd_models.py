from pydantic import BaseModel, validator, EmailStr
from .exceptions import PasswordMismatchException
from fastapi import HTTPException


class UserBase(BaseModel):
    email: EmailStr    


class UserUpgrade(UserBase):
    password1: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    password2: str | None = None
    username: str | None = None

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise HTTPException(status_code=400, detail='passwords dont match')
        return v


class UserSignInPass(UserBase):
    password: str


class UserSignInToken(BaseModel):
    token: str


class UserSignUp(UserBase):
    password1: str
    password2: str
    
    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise HTTPException(status_code=400, detail='passwords dont match')
        return v




class User(UserBase):
    id: int
    username: str | None

    class Config:
        orm_mode = True

class UserAuth(User):
    token: str

class UserList(BaseModel):
    users: list[User] | None = []

    class Config:
        orm_mode = True
