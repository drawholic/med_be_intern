from db.models import User
from .exceptions import (
        PasswordMismatchException,
        UserDoesNotExist,
        AuthenticationException,
        UserAlreadyExists
        )
import os
from .utils import encode_password, check_password
from log import logger
from sqlalchemy.orm import Session, selectinload
from .pd_models import UserSignUp, UserUpgrade, UserSignInPass
from sqlalchemy import select, update, delete, insert
from .auth import AuthToken, token_generate, token_decode
from fastapi import HTTPException

from typing import Callable
import dotenv

dotenv.load_dotenv('.env')


salt = os.getenv('SECRET')

class UserCrud:
    
    async def user_query_id(uid: int, db: Session) -> Callable:
        return await db.execute(select(User).where(User.id == uid).options(selectinload(User.user_companies)))

    async def user_query_email(email: str, db: Session) -> Callable:
        return await db.execute(select(User).where(User.email == email).options(selectinload(User.user_companies)))

    async def get_user_by_email(email: str, db: Session) -> User:
        user = await UserCrud.user_query_email(email, db)
        if user is not None:
            return user.scalars().first()
        else:
            raise UserDoesNotExist

    async def get_user_by_id(uid: int, db: Session) -> User:
        user = await UserCrud.user_query_id(uid, db)
        user = user.scalars().first()
        if user is not None:
            return user
        else:
            raise UserDoesNotExist

    async def check_user_id(uid: int, db: Session) -> bool:
        user = await db.execute(select(User).where(User.id==uid))
        user = user.scalars().first()
        return bool(user)

    async def check_user_email(email: str, db: Session) -> bool:
        user = await db.execute(select(User).where(User.email==email))
        user = user.scalars().first()
        return bool(user)

    async def create_user(user: UserSignUp, db: Session) -> User:
        if await UserCrud.check_user_email(user.email, db):
            raise UserAlreadyExists
        else:
            password = encode_password(user.password1)
            user_db = User(password=password, email=user.email)

            db.add(user_db)

            logger.info(f'user {user.email} is created')

            return user_db

    async def update_user(uid: int, user_data: UserUpgrade, db: Session) -> User:
       
        if await UserCrud.check_user_id(uid, db):
            user_data = user_data.dict(exclude_unset=True)
            
            if 'password1' in user_data.keys():
                user_data['password'] = user_data['password1']
                del user_data['password1']
                del user_data['password2']
            
            u = update(User).where(User.id==uid)
            u = u.values(**user_data)
            u.execution_options(synchronize_session='fetch')
            
            await db.execute(u)
            await db.commit()

            user = await UserCrud.get_user_by_id(uid, db)
            logger.info(f'user {user.username} updated')
            
            return user
   
        else:
            raise UserDoesNotExist

    async def delete_crud(uid: int, db: Session) -> User:
        user = await UserCrud.get_user_by_id(uid, db)
        user_delete = delete(User).where(User.id==uid)
        
        await db.execute(user_delete)
        await db.commit()
         
        logger.info(f'user {user.username} was deleted')
        return user

    async def get_users(skip: int, limit: int, db: Session) -> list[User]:
        users = await db.execute(select(User).options(selectinload(User.user_companies)).offset(skip).limit(limit+skip))
        users = users.scalars().all()
        logger.info('users were listed')
        return users

    async def isAuth0(token: str):
        try:
            token = AuthToken(token.credentials).verify()
            return not token.get('status')
        except HTTPException:
            return False

    async def isToken(token):
        email = token_decode(token)
        return bool(email)

    async def authenticate(token: str, db: Session) -> User:

        if await UserCrud.isAuth0(token):
            email = AuthToken(token.credentials).verify()['email']
            user = await UserCrud.get_user_by_email(email, db)
            return user.id

        elif await UserCrud.isToken(token):
            user = await UserCrud.auth_user_token(token, db)
            return user
        else:
            raise AuthenticationException

    async def auth_user(u: UserSignInPass, db: Session) -> User:
        db_user = await UserCrud.get_user_by_email(u.email, db)
        
        if db_user is None:
            raise UserDoesNotExist
        
        if check_password(u.password, db_user.password):
            return db_user

    async def auth_user_token(token: str, db: Session) -> bool:
        email = token_decode(token)
        db_user = await UserCrud.get_user_by_email(email, db)
        
        return db_user.id






