from pydantic import BaseModel



class UserBase(BaseModel):
    username: str



class UserUpgrade(UserBase):
    password: str


class UserSignInPass(UserUpgrade):
    pass


class UserSignInToken(BaseModel):
    token: str


class UserSignUp(UserUpgrade):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserList(BaseModel):
    users: list[User]

    class Config:
        orm_mode = True
