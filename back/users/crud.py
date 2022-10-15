from db.models import User
from .exceptions import PasswordMismatchException, UserDoesNotExist

def user_query(uid, db):
    return db.query(User).filter(User.id==uid)


def create_user(user, db):
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


def check_user(uid, db):
    user = db.query(user_query(uid, db).exists()).scalar()
    if user:
        return True
    else:
        raise UserDoesNotExist


def update_user(uid, user_data, db):
    if check_user(uid, db):
        user = user_query(uid, db)
        user.update(user_data.dict())
        db.commit()
        #db.refresh(user.first())
        return user.first()
    else:
        raise UserDoesNotExist


def delete_user():
    pass


def get_user(user_id, db):
    
    user = db.query(User).filter(User.id==user_id).first()
    if user is not None:
        return user
    else:
        raise UserDoesNotExist


def get_users( db):
    users = db.query(User)
    return users.all()
