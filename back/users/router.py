from fastapi import APIRouter, Response,  Depends, HTTPException, status
from fastapi.security import HTTPBearer

from db.db import get_db
from sqlalchemy.orm import Session
from .crud import UserCrud
from sqlalchemy.ext.asyncio import AsyncSession

from .pd_models import User,UserList, UserSignUp, UserUpgrade, UserSignInPass
from .auth import token_generate


users = APIRouter(prefix='/users', tags=['Users'])


token_auth = HTTPBearer()


@users.post('/get_token')
async def get_token(user_auth: UserSignInPass, db = Depends(get_db)):
    user = await UserCrud.auth_user(user_auth, db)
    
    if user is not None:
        
        token = token_generate(user.email)
        return token
    else:
        raise HTTPException(status_code=400, detail='authentication error')


@users.get('/private')
async def private(token: str = Depends(token_auth), db: Session = Depends(get_db)):

    await UserCrud.authenticate(token, db)


@users.get('/', response_model=UserList)
async def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = await UserCrud.get_users(skip, limit, db)
    return {'users': users}


@users.get('/{user_id}', response_model=User)
async def retrieve_user(user_id: int, db: Session = Depends(get_db)):
    user = await UserCrud.get_user_by_id(user_id, db)
    return user

@users.post('/')
async def sign_up(user: UserSignUp, db: AsyncSession = Depends(get_db)):
    user = await UserCrud.create_user(user, db)
    if user is not None:
        await db.commit()
    else:
        await db.rollback()
        raise HTTPException


@users.patch('/{uid}')
async def edit_user(
        uid: int,
        user_upd: UserUpgrade,
        token: str = Depends(token_auth),
        db: Session = Depends(get_db)) -> User:

    await UserCrud.authenticate(token, db)
    user = await UserCrud.update_user(uid, user_upd, db)
    return user


@users.delete('/{user_id}')
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        token: str = Depends(token_auth)):

    await UserCrud.authenticate(token, db)
    await UserCrud.delete_crud(user_id, db)


