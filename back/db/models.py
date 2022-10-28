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
    email = Column(String, nullable=False, unique=True)

    user_companies = relationship('Company', backref='owner')


    # joined_companies = relationship('Company', backref='participants')
    # invitations = relationship('Company', backref='invited_users')


class Company(BaseModel):
    __tablename__ = 'companies'

    title = Column(String)
    description = Column(String)
    hidden = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

    admins = relationship('User', backref='being_admin')
    # participants = relationship('User', backref='in_companies' )
    # requests = relationship('User', backref='requests')














