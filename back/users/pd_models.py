from pydantic import BaseModel, validator, EmailStr
from .exceptions import PasswordMismatchException
from fastapi import HTTPException


class UserBase(BaseModel):
    email: EmailStr    


class UserUpgrade(UserBase):
    password1: str | None
    username: str | None
    email: EmailStr | None
    password2: str | None 
    username: str | None

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
    password_confirm: str
    password: str
    


class User(UserBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: list[User] | None = []

    class Config:
        orm_mode = True
