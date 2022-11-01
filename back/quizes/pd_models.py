from pydantic import BaseModel, validator
from datetime import datetime
from .exceptions import AnswersQuantityException, QuestionsQuantityException


class AnswerBase(BaseModel):
    text: str
    question_id: int
    correct: bool

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    text: str
    quiz_id: int

class QuestionCreate(QuestionBase):
    answers: list[AnswerCreate]
class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class QuestionDetail(Question):
    answers: list[Answer] | None = []

    class Config:
        orm_mode = True


class QuizBase(BaseModel):
    title: str
    description: str
    company_id: int
    frequency: int

class QuizCreate(QuizBase):
    questions: list[QuestionCreate]

class Quiz(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class QuizDetail(Quiz):
    questions: list[Question] | None = []

    class Config:
        orm_mode = True

