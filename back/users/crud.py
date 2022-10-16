from db.models import User
from .exceptions import PasswordMismatchException, UserDoesNotExist, UserAlreadyExists

def user_query(uid, db):
    return db.query(User).filter(User.id==uid)


def check_user(uid, db):
    user = db.query(user_query(uid, db).exists()).scalar()
    if user:
        return True
    else:
        raise UserDoesNotExist


def create_user(user, db):
    if db.query(User).filter(User.username==user.username).first():
        raise UserAlreadyExists
    else:
        password1 = user.password
        password2 = user.password_confirm
        username = user.username
        email = user.email
        if password1 == password2:
            password = str(hash(password1))
            user_db = User(username=username, password=password, email=email)
            db.add(user_db)
            db.commit()
            db.refresh(user_db)
            return user_db
        else: 
            raise PasswordMismatchException


def update_user(uid, user_data, db):
    if check_user(uid, db):
        user = user_query(uid, db)
        user.update(user_data.dict())
        db.commit()
        return user.first()
    else:
        raise UserDoesNotExist


def delete_user(uid, db):
    user = user_query(uid, db).first()
    db.delete(user)



def get_user(user_id, db):
    
    user = db.query(User).filter(User.id==user_id).first()
    if user is not None:
        return user
    else:
        raise UserDoesNotExist


def get_users(skip, limit, db):
    users = db.query(User).limit(skip+limit).offset(skip)
    return users.all()


