from db.models import User
from .exceptions import PasswordMismatchException, UserDoesNotExist, UserAlreadyExists
from log import logger
from sqlalchemy.orm import Session
from .exceptions import UserAlreadyExists


def user_query_id(uid, db):
    return db.query(User).filter(User.id==uid)


def user_query_mail(mail, db):
    return db.query(User).filter(User.email==mail)


def check_user_id(uid, db):
    user = db.query(user_query_id(uid, db).exists()).scalar()
    if user:
        return True
    else:
        return False


def check_user_mail(mail, db):
    user = db.query(user_query_mail(mail, db).exists()).scalar()
    if user:
        return True
    else:
        return False


def create_user(user, db):
    if check_user_mail(user.email, db):
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

    if check_user_id(uid, db):
        user = user_query_id(uid, db)
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


def delete_crud(uid: int, db: Session):
    user = user_query_id(uid, db).first()
    db.delete(user)
    db.commit()
    logger.info(f'user {user.username} was deleted')
    return user



def get_user(uid: int, db: Session):
    
    user = user_query_id(uid, db).first()
    
    if user is not None:
        return user
    
    else:
        raise UserDoesNotExist

def get_user_by_email(mail: str, db: Session):
    user = user_query_mail(mail, db).first()

    if user is not None:
        return user
    else:
        raise UserDoesNotExist


def get_users(skip: int, limit: int, db: Session):
    users = db.query(User).limit(skip+limit).offset(skip)
    logger.info('users were listed')
    return users.all()



def auth_user(u, db: Session):
    db_user = get_user_by_email(u.email, db)
    user_pass = str(hash(u.password))
    print('first here')
    if db_user.password == user_pass and db_user.email == u.email:
        return db_user
        print('here')     








