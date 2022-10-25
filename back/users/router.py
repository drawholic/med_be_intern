from fastapi import APIRouter, Response,  Depends, HTTPException, status
from fastapi.security import HTTPBearer
import hashlib
from db.db import get_db
from sqlalchemy.orm import Session
from .crud import UserCrud

from .pd_models import User, UserList, UserAuth, UserSignUp, UserUpgrade, UserSignInPass
from .auth import AuthToken, token_generate, token_decode


users = APIRouter(prefix='/users')


token_auth = HTTPBearer()


@users.post('/get_token')
async def auth_route(user_auth: UserSignInPass, db = Depends(get_db)) -> str:
    user = await UserCrud.auth_user(user_auth, db)
    
    if user is not None:
        
        token = token_generate(user.email)
        return token 
    else:
        raise HTTPException(status_code=400, detail='authentication error')




@users.get('/private', response_model=User)
async def private(response: Response, token: str = Depends(token_auth), db: Session = Depends(get_db)):
    return await UserCrud.authenticate(token, db)


@users.get('/', response_model=list[User])
async def list_users(skip:int = 0, limit:int = 10, db = Depends(get_db))-> list[User] | None:

    return await UserCrud.get_users(skip, limit, db)
    


@users.get('/{user_id}', response_model=User)
async def retrieve_user(user_id: int, db = Depends(get_db)) -> User:
    
    return await UserCrud.get_user_by_id(user_id, db)
    


@users.post('/', response_model=User)
async def sign_up(user: UserSignUp, db=Depends(get_db)) -> User:
    
    return await UserCrud.create_user(user, db)
    


@users.patch('/{uid}', response_model=User)
async def edit_user(
        uid: int, 
        user_upd: UserUpgrade,
        token: str = Depends(token_auth), db = Depends(get_db)) -> User:

    if await UserCrud.auth_user_token(token, db):
        user = await UserCrud.update_user(uid, user_upd, db)
        return user
    else:
        raise HTTPException(status_code=400, detail='authentication error')        


@users.delete('/{user_id}', response_model=User)
async def delete_user(
        user_id:int, 
        db = Depends(get_db), 
        token: str = Depends(token_auth)) -> User:
        
    user = await UserCrud.auth_user_token(token, db)
    if user.id == user_id:
        user = await UserCrud.delete_crud(user_id, db)
        return user
    else:
        raise HTTPException(status_code=400, detail='authentication error')


