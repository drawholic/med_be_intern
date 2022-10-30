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

    user_companies = relationship('Owner', back_populates='owner')
    in_companies = relationship('Participants', back_populates='participant')
    invitations = relationship('Invitations', back_populates='user')


class Company(BaseModel):
    __tablename__ = 'companies'

    title = Column(String, unique=True)
    description = Column(String)
    hidden = Column(Boolean, default=False)
    owner = relationship('Owner', back_populates='company')
    participants = relationship('Participants', back_populates='company')
    invited_users = relationship('Invitations', back_populates='company')


class Owner(BaseModel):
    __tablename__ = 'owners'
    owner_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)

    owner = relationship('User', back_populates='user_companies')
    company = relationship('Company', back_populates='owner')


class Participants(BaseModel):
    __tablename__ = 'participants'

    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    participant_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    company = relationship('Company', back_populates='participants')
    participant = relationship('User', back_populates='in_companies')


class Invitations(BaseModel):
    __tablename__ = 'invitations'

    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    user = relationship("User", back_populates='invitations')
    company = relationship('Company', back_populates='invited_users')