from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False,unique=True)
    
