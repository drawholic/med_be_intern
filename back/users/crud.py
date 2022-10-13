from db.models import User



def get_user(user_id, db):
    return db.query(User).filter(User.id==user_id).first()



def get_users(db):
    return db.query(User).all()
