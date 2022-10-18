from db.models import User
from .exceptions import PasswordMismatchException, UserDoesNotExist, UserAlreadyExists
from log import logger
from sqlalchemy.orm import Session
from .exceptions import UserAlreadyExists

def user_query(uid, db):
    return db.query(User).filter(User.id==uid)


def check_user(uid, db):
    user = db.query(user_query(uid, db).exists()).scalar()
    if user:
        return True
    else:
        raise UserDoesNotExist


def create_user(user, db):
    if db.query(User).filter(User.email==user.email).first():
        raise UserAlreadyExists
    else:
        password1 = user.password1
        password2 = user.password2
        email = user.email
        if password1 == password2:
            password = str(hash(password1))
            user_db = User(password=password, email=email)
            db.add(user_db)
            db.commit()
            db.refresh(user_db)
            logger.info(f'user {email} is created')
            return user_db
        else: 
            raise PasswordMismatchException


def update_user(uid: int, user_data, db):

    if check_user(uid, db):
        user = user_query(uid, db)
        user_data = user_data.dict(exclude_unset=True)
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


def delete_crud(uid: int, db: Session):
    user = user_query(uid, db).first()
    db.delete(user)
    db.commit()
    logger.info(f'user {user.username} was deleted')
    return user



def get_user(uid: int, db: Session):
    
    user = user_query.first()
    
    if user is not None:
        return user
    
    else:
        raise UserDoesNotExist


def get_users(skip: int, limit: int, db: Session):
    users = db.query(User).limit(skip+limit).offset(skip)
    logger.info('users were listed')
    return users.all()



def auth_user(uid:int, u, db):
    db_user = user_query(uid, db).first()
    user_pass = str(hash(u['password']))
    if db_user['password'] == user_pass and db_user['email'] == u['email']:
        return db_user
        








