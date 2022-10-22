from db.models import User
from .exceptions import PasswordMismatchException, UserDoesNotExist, UserAlreadyExists
from log import logger
from sqlalchemy.orm import Session
from .exceptions import UserAlreadyExists
from .pd_models import UserSignUp, UserUpgrade, UserSignInPass
from sqlalchemy import select, update, delete



from typing import Callable

class UserCrud:
    
    async def user_query_id(uid: int, db: Session) -> Callable:
        return await db.execute(select(User).where(User.id==uid))
    
    async def user_query_email(email: str, db: Session) -> Callable:
        return await db.execute(select(User).where(User.email==email))

            
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
        user = await UserCrud.user_query_id(uid, db)
        user = user.scalars().first()
        return bool(user)
    

    async def check_user_email(email: str, db: Session) -> bool:
        user = await UserCrud.user_query_email(email, db)
        user = user.scalars().first()
        return bool(user)


    async def create_user(user: UserSignUp, db: Session) -> User:
        if await UserCrud.check_user_email(user.email, db):
            raise UserAlreadyExists
        else:
            password = str(hash(user.password1))
            user_db = User(password=password, email=user.email)
            db.add(user_db)
            await db.commit()
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
        users = await db.execute(select(User))
        users = users.scalars().all()

        logger.info('users were listed')
        return users
    
    async def auth_user(u: UserSignInPass, db: Session) -> User:
        db_user = await UserCrud.get_user_by_email(u.email, db)
        user_pass = str(hash(u.password))
        if db_user.password == user_pass and db_user.email == u.email:
            return db_user








