from fastapi import APIRouter, Response,  Depends, HTTPException, status
from fastapi.security import HTTPBearer

from db.db import get_db
from sqlalchemy.orm import Session
from .crud import UserCrud


from .pd_models import User, UserList, UserAuth, UserSignUp, UserUpgrade, UserSignInPass
from .exceptions import PasswordMismatchException, UserDoesNotExist, UserAlreadyExists
from .auth import VerifyToken, token_generate, token_decode

users = APIRouter(prefix='/users')


token_auth = HTTPBearer()


@users.post('/auth', response_model=UserAuth)
async def auth_route(user_auth: UserSignInPass, db = Depends(get_db)) -> User:
    user = UserCrud.auth_user(user_auth, db)
    
    if user is not None:
        
        token = token_generate(user.email)
        user.token = token
        return user
    else:
        raise HTTPException(status_code=400, detail='authentication error')


@users.get('/private')
async def private(response: Response, token: str = Depends(token_auth), db: Session = Depends(get_db)):
    
    result = VerifyToken(token.credentials).verify()
    
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    if result.get('email'):
        user = UserCrud.get_user_by_email(result.get('email'), db) 
        return user


    return result


@users.get('/',response_model=list[User])
async def list_users(skip:int = 0, limit:int = 10, db = Depends(get_db)) -> list[User]:
    
    try:
        return get_users(skip, limit, db)
    
    except Exception as e:
        raise HTTPException(status_code=400) 


@users.get('/{user_id}', response_model=User)
async def retrieve_user(user_id: int, db = Depends(get_db)) -> User:
    
    return UserCrud.get_user_by_id(user_id, db)
    


@users.post('/', response_model=User)
async def sign_up(user: UserSignUp, db=Depends(get_db)) -> User:
    
    return UserCrud.create_user(user, db)
    


@users.patch('/{uid}', response_model=User)
async def edit_user(uid: int, user_upd: UserUpgrade, db = Depends(get_db)) -> User:

    user = UserCrud.update_user(uid, user_upd, db)
    return user
        


@users.delete('/{user_id}', response_model=User)
async def delete_user(user_id:int, db = Depends(get_db)) -> User:
    
    try:
        user = delete_crud(user_id, db)
        return user
    
    except Exception as e:
        logger.debug(e) 
        raise HTTPException(status_code=400)


