from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,Boolean, String, Column, DateTime
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
    companies = relationship('Company', backref='owner')
    requests = relationship('Company', backref='invited')


class Company(BaseModel):
    __tablename__ = 'companies'

    title = Column(String)
    description = Column(String)
    hidden = Column(Boolean, default=False)
    invited = relationship('User', backref='requests')
    admins = relationship('User', backref='')
    requests = relationship('User')
