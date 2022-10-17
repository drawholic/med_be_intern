from fastapi import APIRouter, Response,  Depends, HTTPException, status
from fastapi.security import HTTPBearer

from db.db import get_db

from .crud import get_users, get_user, create_user, update_user, delete_crud
from .pd_models import User, UserList, UserSignUp, UserUpgrade
from .exceptions import PasswordMismatchException, UserDoesNotExist
from .auth import VerifyToken

users = APIRouter(prefix='/users')


token_auth = HTTPBearer()

@users.get('/private')
async def private(response: Response, token:str = Depends(token_auth)):
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result

    return result

@users.get('/',response_model=list[User])
async def list_users(skip:int = 0, limit:int = 10, db = Depends(get_db)):
    
    try:
        return get_users(skip, limit, db)
    
    except Exception as e:
        raise HTTPException(status_code=400) 


@users.get('/{user_id}', response_model=User)
async def retrieve_user(user_id: int, db = Depends(get_db)):
    
    try:
        return get_user(user_id, db)
    
    except UserDoesNotExist:
        raise HTTPException(status_code=404, detail='User is not found')


@users.post('/', response_model=User)
async def sign_up(user: UserSignUp, db=Depends(get_db)):
    
    try:
        return create_user(user, db)
    
    except PasswordMismatchException:
        raise HTTPException(status=400, detail='Passwords do not match')
    
    except UserAlreadyExists:
        raise HTTPException(status=400, detail='Username is already taken')


@users.patch('/{uid}', response_model=User)
async def edit_user(uid: int, user_upd: UserUpgrade, db = Depends(get_db)):
    

    try:
        user = update_user(uid, user_upd, db)
        return user
        
    except UserDoesNotExist:
        raise HTTPException(status_code=400, detail='User does not exist')
    
    except PasswordMismatchException:
        raise HTTPException(status_code=400, detail='Passwords do not match')


@users.delete('/{user_id}', response_model=User)
async def delete_user(user_id:int, db = Depends(get_db)):
    try:
        user = delete_crud(user_id, db)
        return user
    except Exception as e:
        logger.debug(e) 
        raise HTTPException(status_code=400)


