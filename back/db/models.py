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
    being_admin = relationship('Admin', back_populates='user')
    company_requests = relationship('Requests', back_populates='user')


class Company(BaseModel):
    __tablename__ = 'companies'

    title = Column(String, unique=True)
    description = Column(String)
    hidden = Column(Boolean, default=False)

    owner = relationship('Owner', back_populates='company')
    participants = relationship('Participants', back_populates='company')
    invited_users = relationship('Invitations', back_populates='company')
    admins = relationship('Admin', back_populates='company')
    users_requests = relationship('Requests', back_populates='company')
    quizes = relationship("Quiz", back_populates='company')


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


class Admin(BaseModel):
    __tablename__ = 'admins'

    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    user = relationship('User', back_populates='being_admin')
    company = relationship('Company', back_populates='admins')


class Requests(BaseModel):
    __tablename__ = 'requests'

    company_id = Column(Integer, ForeignKey('companies.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    user = relationship('User', back_populates='company_requests')
    company = relationship('Company', back_populates='users_requests')


class Quiz(BaseModel):
    __tablename__ = 'quizes'

    title = Column(String)
    description = Column(String)
    frequency = Column(Integer)

    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship('Company', back_populates='quizes')
    questions = relationship('Question', back_populates='quiz')


class Question(BaseModel):
    __tablename__ = 'questions'

    text = Column(String)
    quiz_id = Column(Integer, ForeignKey('quizes.id'))

    quiz = relationship('Quiz', back_populates='questions')
    answers = relationship('Answer', back_populates='question')


class Answer(BaseModel):
    __tablename__ = 'answers'

    question_id = Column(Integer, ForeignKey('questions.id'))

    question = relationship('Question', back_populates='answers')
    text = Column(String)
    correct = Column(Boolean, default=False)