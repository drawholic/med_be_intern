from db.models import User, Company, Invitations, Participants, Owner
from .exceptions import (
        UserDoesNotExist,
        AuthenticationException,
        UserAlreadyExists
        )
import os
from .utils import encode_password, check_password
from log import logger
from sqlalchemy.orm import selectinload
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

    async def user_query_id(self, uid: int) -> Callable:
        return await self.db.execute(
            select(User)
            .where(User.id == uid))

    async def user_query_email(self, email: str) -> Callable:
        return await self.db.execute(
            select(User)
            .where(User.email == email)
        )

    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_query_email(email)
        user = user.scalars().first()
        if user is not None:
            return user
        else:
            raise UserDoesNotExist

    async def get_user_by_id(self, uid: int) -> User:
        user = await self.user_query_id(uid)
        user = user.scalars().first()
        if user is not None:
            return user
        else:
            raise UserDoesNotExist

    async def check_user_id(self, uid: int) -> bool:
        user = await self.db.execute(select(User).where(User.id==uid))
        user = user.scalars().first()
        return bool(user)

    async def check_user_email(self, email: str) -> bool:
        user = await self.db.execute(select(User).where(User.email==email))
        user = user.scalars().first()
        return bool(user)

    async def create_user(self, user: UserSignUp) -> User:
        if await self.check_user_email(user.email):
            raise UserAlreadyExists
        else:
            password = encode_password(user.password1)
            user_db = User(password=password, email=user.email)

            self.db.add(user_db)

            logger.info(f'user {user.email} is created')
            return user_db

    async def update_user(self, uid: int, user_data: UserUpgrade) -> User:
       
        if await self.check_user_id(uid):
            user_data = user_data.dict(exclude_unset=True)
            
            if 'password1' in user_data.keys():
                user_data['password'] = user_data['password1']
                del user_data['password1']
                del user_data['password2']
            
            u = update(User).where(User.id==uid)
            u = u.values(**user_data)
            u.execution_options(synchronize_session='fetch')
            
            await self.db.execute(u)
            await self.db.commit()

            user = await self.get_user_by_id(uid)
            logger.info(f'user {user.username} updated')
            
            return user
   
        else:
            raise UserDoesNotExist

    async def delete_crud(self, uid: int) -> User:
        user = await self.get_user_by_id(uid)
        user_delete = delete(User).where(User.id == uid)
        
        await self.db.execute(user_delete)
        await self.db.commit()
         
        logger.info(f'user {user.username} was deleted')
        return user

    async def get_users(self, skip: int, limit: int) -> list[User]:
        users = await self.db.execute(select(User).offset(skip).limit(limit+skip))
        users = users.scalars().all()

        logger.info('users were listed')
        return users

    async def isAuth0(self, token: str):
        try:
            token = AuthToken(token.credentials).verify()
            return not token.get('status')
        except HTTPException:
            return False

    async def isToken(self, token):
        email = token_decode(token)
        return bool(email)

    async def authenticate(self, token: str) -> User:

        if await self.isAuth0(token):
            email = AuthToken(token.credentials).verify()['email']
            user = await self.get_user_by_email(email)
            return user.id

        elif await self.isToken(token):
            user = await self.auth_user_token(token)
            return user
        else:
            raise AuthenticationException

    async def auth_user(self, u: UserSignInPass) -> User:
        db_user = await self.get_user_by_email(u.email)
        
        if db_user is None:
            raise UserDoesNotExist
        
        if check_password(u.password, db_user.password):
            return db_user

    async def auth_user_token(self, token: str) -> bool:
        email = token_decode(token)
        db_user = await self.get_user_by_email(email)

        return db_user.id

    async def get_invitations(self, u_id: int):
        # get all invitations
        stm = select(Invitations.company).options(selectinload(Invitations.company)).where(Invitations.user_id == u_id)
        invitations = await self.db.execute(stm)
        invitations = invitations.scalars().all()
        return invitations

    async def accept_invitation(self, i_id: int):
        # get invitation
        stm = select(Invitations).where(Invitations.id == i_id)
        invitation = await self.db.execute(stm)
        invitation = invitation.scalars().first()
        # creating participant
        stm = insert(Participants).values(company_id=invitation.company_id, participant_id=invitation.user_id)
        await self.db.execute(stm)
        # deleting invitation
        stm = delete(Invitations).where(Invitations.id == i_id)
        await self.db.execute(stm)
        return {'status': 'invitation accepted'}






