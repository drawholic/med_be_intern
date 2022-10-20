from db.models import User
from .exceptions import PasswordMismatchException, UserDoesNotExist, UserAlreadyExists
from log import logger
from sqlalchemy.orm import Session
from .exceptions import UserAlreadyExists
from .pd_models import UserSignUp, UserUpgrade, UserSignInPass

from typing import Callable

class UserCrud:
    
    def user_query_id(uid: int, db: Session) -> Callable:
        return db.query(User).filter(User.id==uid)
    
    def user_query_email(email: str, db: Session) -> Callable:
        return db.query(User).filter(User.email==email)

            
    def get_user_by_email(email: str, db: Session) -> User:
        user = UserCrud.user_query_email(email, db).first()
        if user is not None:
            return user
        else:
            raise UserDoesNotExist


    def get_user_by_id(uid: int, db: Session) -> User:
        user = UserCrud.user_query_id(uid, db).first()
        if user is not None:
            return user
        else:
            raise UserDoesNotExist

    def check_user_id(uid: int, db: Session) -> bool:
        user = db.query(UserCrud.user_query_id(uid, db).exists()).scalar()
        if user:
            return True
        else:
            return False
    
    def check_user_email(email: str, db: Session) -> bool:
        user = db.query(UserCrud.user_query_email(email, db).exists()).scalar()
        if user:
            return True
        else:
            return False
    
    def create_user(user: UserSignUp, db: Session) -> User:
        if UserCrud.check_user_email(user.email, db):
            raise UserAlreadyExists
        else:
            user_db = User(password=user.password1, email=user.email)
            db.add(user_db)
            db.commit()
            db.refresh(user_db)
            logger.info(f'user {user.email} is created')
            return user_db

    def update_user(uid: int, user_data: UserUpgrade, db: Session) -> User:
        
        if UserCrud.check_user_id(uid, db):
            user = UserCrud.user_query_id(uid, db)
            user_data = user_data.dict(exclude_unset=True)
            if 'password1' in user_data.keys():
                user_data['password'] = user_data['password1']
                del user_data['password1']
                del user_data['password2']
            user.update(user_data)
            user = user.first()
            db.commit()
            logger.info(f'user {user.username} updated')
            return user
   
        else:
            raise UserDoesNotExist

    def delete_crud(uid: int, db: Session) -> User:
        user = user_query_id(uid, db).first()
        db.delete(user)
        db.commit()
        logger.info(f'user {user.username} was deleted')
        return user
    
    def get_users(skip: int, limit: int, db: Session) -> list[User]:
        users = db.query(User).limit(skip + limit).offset(skip).all()
        logger.info('users were listed')
        return users
    
    def auth_user(u: UserSignInPass, db: Session) -> User:
        db_user = get_user_by_email(u.email, db)
        user_pass = str(hash(u.password))
        if db_user.password == user_pass and db_user.email == u.email:
            return db_user








