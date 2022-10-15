from fastapi import APIRouter, Depends, HTTPException
from db.db import get_db
from .crud import get_users, get_user, create_user, update_user
from .pd_models import User, UserList, UserSignUp, UserUpgrade
from .exceptions import PasswordMismatchException, UserDoesNotExist

users = APIRouter(prefix='/users')


@users.get('/',
        response_model=list[User]
        )
async def list_users(db = Depends(get_db)):
    try:
        return get_users(db)
    except Exception as e:
        return HTTPException(status_code=400) 


@users.get('/{user_id}', 
        #response_model=User
        )
async def retrieve_user(user_id: int, db = Depends(get_db)):
    try:
        return get_user(user_id, db)
    except UserDoesNotExist:
        return HTTPException(status_code=404, detail='User is not found')


@users.post('/',
        #response_model=User
        # не можу зробити response model. Якщо роблю exception, то responsemodel не валідує
        # те саме і вище
        )
async def sign_up(user: UserSignUp, db=Depends(get_db)):
    try:
        return create_user(user, db)
    except PasswordMismatchException:
        raise HTTPException(status=400, detail='Passwords do not match')


@users.put('/{user_id}', )
async def edit_user(user_id: int, user_upd: UserUpgrade, db = Depends(get_db)):
    try:
        user = update_user(user_id, user_upd, db)
        return user
    except UserDoesNotExist:
        return HTTPException(status_code=400, detail='User does not exist')






