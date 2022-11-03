from db.models import User, Company, Invitations, Participants, Owner
from .exceptions import (
        UserDoesNotExist,
        AuthenticationException,
        UserAlreadyExists
        )
import os
from .utils import encode_password, check_password
from log import logger
from .pd_models import UserSignUp, UserUpgrade, UserSignInPass 
from sqlalchemy import select, update, delete, insert
from .auth import AuthToken, token_decode

from fastapi import HTTPException 

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Callable
import dotenv

dotenv.load_dotenv('.env')


salt = os.getenv('SECRET') 


class UserCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def user_query_id(self, uid: int) -> User:
        return await self.db.execute(
            select(User)
            .where(User.id == uid))

    async def user_query_email(self, email: str) -> User:
        return await self.db.execute(
            select(User)
            .where(User.email == email)
        )

    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_query_email(email=email)
        user = user.scalars().first()
        if user is not None:
            return user
        else:
            raise UserDoesNotExist

    async def get_user_by_id(self, uid: int) -> User:
        user = await self.user_query_id(uid=uid)
        user = user.scalars().first()
        if user is not None:
            return user
        else:
            raise UserDoesNotExist

    async def check_user_id(self, uid: int) -> bool:
        user = await self.db.execute(select(User).where(User.id == uid))
        user = user.scalars().first()
        return bool(user)

    async def check_user_email(self, email: str) -> bool:
        user = await self.db.execute(select(User).where(User.email == email))
        user = user.scalars().first()
        return bool(user)

    async def create_user(self, user: UserSignUp) -> User:
        if await self.check_user_email(email=user.email):
            raise UserAlreadyExists
        else: 
            password = encode_password(password=user.password1)
            stm = insert(User).returning(User).values(password=password, email=user.email)
            result = await self.db.execute(stm)
            logger.info(f'user {user.email} is created')
            return result

    async def update_user(self, uid: int, user_data: UserUpgrade) -> User:
       
        if await self.check_user_id(uid=uid):
            user_data = user_data.dict(exclude_unset=True)
            
            if 'password1' in user_data.keys():
                user_data['password'] = user_data['password1']
                del user_data['password1']
                del user_data['password2']
            
            u = update(User).where(User.id == uid)
            u = u.values(**user_data)
            u.execution_options(synchronize_session='fetch')
            
            await self.db.execute(u)
            await self.db.commit()

            user = await self.get_user_by_id(uid=uid)
            logger.info(f'user {user.username} updated')
            
            return user
   
        else:
            raise UserDoesNotExist

    async def delete_crud(self, uid: int) -> User:
        user = await self.get_user_by_id(uid=uid)
        user_delete = delete(User).where(User.id == uid)
        
        await self.db.execute(user_delete)
        await self.db.commit()
         
        logger.info(f'user {user.username} was deleted')
        return user

    async def get_users(self, skip: int, limit: int) -> list[User]:
        users = await self.db.execute(select(User).offset(skip).limit(limit))
        users = users.scalars().all()

        logger.info('users were listed')
        return users
 
    async def isAuth0(self, token: str) -> bool:
        try:
            token = AuthToken(token.credentials).verify()
            return not token.get('status')
        except HTTPException:
            return False

    async def isToken(self, token) -> bool:
        email = token_decode(token=token)
        return bool(email)

    async def authenticate(self, token: str) -> User:

        if await self.isAuth0(token=token):
            email = AuthToken(token.credentials).verify().get('email') 
            user = await self.get_user_by_email(email=email) 
            return user.id

        elif await self.isToken(token=token):
            user = await self.auth_user_token(token=token)
            return user
        else:
            raise AuthenticationException

    async def auth_user(self, u: UserSignInPass) -> User:
        db_user = await self.get_user_by_email(email=u.email)
        
        if db_user is None:
            raise UserDoesNotExist
        
        if check_password(password=u.password, user_password=db_user.password):
            return db_user

    async def auth_user_token(self, token: str) -> int:
        email = token_decode(token=token)
        db_user = await self.get_user_by_email(email=email)

        return db_user.id








