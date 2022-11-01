from fastapi import APIRouter, Response,  Depends, HTTPException, status
from fastapi.security import HTTPBearer

from db.models import User
from db.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import UserCrud

from .pd_models import User as UserPD, UserSignUp, UserUpgrade, UserSignInPass
from .auth import token_generate 


users = APIRouter(prefix='/users', tags=['Users'])


token_auth = HTTPBearer()


@users.post('/get_token') 
async def get_token(user_auth: UserSignInPass, db: AsyncSession = Depends(get_db)) -> str:
    user = await UserCrud(db=db).auth_user(u=user_auth)
    
    if user is not None:
        
        token = token_generate(payload=user.email)
        return token 
    else:
        raise HTTPException(status_code=400, detail='authentication error')

 
@users.get('/private')
async def private(token: str = Depends(token_auth), db: Session = Depends(get_db)):
    await UserCrud(db=db).authenticate(token=token)


@users.get('/', response_model=list[UserPD])
async def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[User]:
    return await UserCrud(db=db).get_users(skip=skip, limit=limit)


@users.get('/{user_id}', response_model=UserPD)
async def retrieve_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = await UserCrud(db=db).get_user_by_id(uid=user_id)
    return user


@users.post('/')
async def sign_up(user: UserSignUp, db: AsyncSession = Depends(get_db)):
    user = await UserCrud(db=db).create_user(user=user)
    if user is not None:

        await db.commit()
        return user
    else:
        await db.rollback()
        raise HTTPException


@users.patch('/{uid}', response_model=UserPD)
async def edit_user(
        uid: int,
        user_upd: UserUpgrade,
        token: str = Depends(token_auth),
        db: Session = Depends(get_db)) -> User:

    await UserCrud(db=db).authenticate(token=token)
    user = await UserCrud(db=db).update_user(uid=uid, user_data=user_upd)
    return user 


@users.delete('/{user_id}')
async def delete_user( 
        user_id: int,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(token_auth)) -> None:

    await UserCrud(db=db).authenticate(token=token)
    await UserCrud(db=db).delete_crud(uid=user_id)


