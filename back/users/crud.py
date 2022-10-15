from db.models import User
from .exceptions import PasswordMismatchException

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
    else: 
        raise PasswordMismatchException

def update_user(user, db):
    pass

def delete_user():
    pass


def get_user(user_id, db):
    return db.query(User).filter(User.id==user_id).first()


def get_users( db):
    users = db.query(User)
    print(users.count())
    return users.all()
