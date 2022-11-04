from pydantic import BaseModel, validator
from datetime import datetime
from .exceptions import AnswersQuantityException,CorrectAnswersQuantityException, QuestionsQuantityException


class AnswerBase(BaseModel):
    text: str
    correct: bool

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    answers: list[AnswerCreate]

    @validator('answers')
    def answers_quantity(cls, v, values):
        if len(v) < 2:
            raise AnswersQuantityException
        return v
    @validator('answers')
    def correct_answers(cls, v, values):
        correct_answers = filter( lambda answer: answer.correct == True , v)
        correct_answers_length = len(list(correct_answers))
        if correct_answers_length > 1 or correct_answers_length < 1:
            raise CorrectAnswersQuantityException
        return v

    class Config:
        orm_mode = True

class Question(QuestionBase):
    quiz_id: int
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True

class QuestionDetail(Question):
    answers: list[Answer]


class QuizBase(BaseModel):
    title: str
    description: str
    company_id: int
    frequency: int

class QuizUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    frequency: int | None = None

class QuizCreate(QuizBase):
    questions: list[QuestionCreate]

    @validator('questions')
    def questions_quantity(cls, v, values):
        if len(v) < 2:
            raise QuestionsQuantityException
        return v

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

