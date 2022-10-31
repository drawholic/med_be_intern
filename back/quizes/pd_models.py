from pydantic import BaseModel, validator
from datetime import datetime
from .exceptions import AnswersQuantityException


class AnswerBase(BaseModel):
    text: str
    question_id: int

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
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class QuestionDetail(QuestionBase):
    answers: list[Answer] | None = []


    @validator('answers')
    def answers_quantity(cls, v, values):
        quantity = None
        if v in values:
            quantity = len(v)
        if quantity < 2 or quantity > 6:
            raise AnswersQuantityException

    class Config:
        orm_mode = True


class QuizBase(BaseModel):
    title: str
    description: str
    company_id: int
    frequency: int

class QuizCreate(QuizBase):
    pass

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

