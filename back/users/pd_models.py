from pydantic import BaseModel, validator, EmailStr
from .exceptions import PasswordMismatchException
from fastapi import HTTPException


class UserBase(BaseModel):
    email: EmailStr    


class UserUpgrade(BaseModel):

    username: str | None = None
    password1: str | None = None
    password2: str | None = None

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



