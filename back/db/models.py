from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey, Boolean, String, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False,unique=True)
    
    #companies = relationship('Company', backref='own')
    

class Owner(BaseModel):
    __tablename__ = 'owners'

    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))


class Invitation(BaseModel):
    __tablename__ = 'invitations'

    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))


class RequestToJoin(BaseModel):
    __tablename__ = 'requests'
    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))


class Admin(BaseModel):
    __tablename__ = 'admins'
    admin_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))


class Company(BaseModel):
    __tablename__ = 'companies'

    title = Column(String)
    description = Column(String)
    hidden = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey('users.id'))        

    













