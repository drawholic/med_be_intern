from fastapi import APIRouter, Depends
from db.db import get_db
from .crud import get_users, get_user, create_user
from .pd_models import User, UserList, UserSignUp
from .exceptions import PasswordMismatchException
users = APIRouter(prefix='/users')


@users.get('/', response_model=UserList)
async def list_users(db = Depends(get_db)):
    try:
        return get_users(db)
    except Exception as e:
        print(e)
        return {"msg":'Bad Request', 'status':400, "detail": e}
        


@users.get('/{user_id}', response_model=User)
async def retrieve_user(user_id: int, db = Depends(get_db)):
    try:
        return get_user(user_id, db)
    except Exception as e:
        print(e)
        return {'msg': 'Bad Request', 'status':400, 'detail':e}


@users.post('/', response_model=User)
async def sign_up(user: UserSignUp, db=Depends(get_db)):
    try:
        return create_user(user, db)
    except PasswordMismatchException:
        raise HTTPException(status=400, detail='password do not match')
