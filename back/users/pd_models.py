from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    username: str
    


class UserUpgrade(UserBase):
    password: str


class UserSignInPass(UserUpgrade):
    pass


class UserSignInToken(BaseModel):
    token: str


class UserSignUp(UserUpgrade):
    password_confirm: str
    email: EmailStr


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserList(BaseModel):
    users: list[User] | None = []

    class Config:
        orm_mode = True
