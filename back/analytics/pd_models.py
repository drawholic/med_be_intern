from pydantic import BaseModel
from datetime import datetime


class QuizMean(BaseModel):
    question_id: int
    mean_results: float


class CompanyQuizMean(BaseModel):
    company_id: int
    mean_results: float


class UserQuizMean(BaseModel):
    user_id: int
    mean_results: float


class UserLatestQuizResult(BaseModel):
    user_id: int
    latest_result: float


class UsersCompanyMean(UserQuizMean):
    user_id: int
    mean_results: float
    quiz_id: int

    class Config:
        orm_mode = True


class UsersLatestQuiz(BaseModel):
    user_id: int
    quiz_id: int
    quiz_latest: int


class UserQuizMean(BaseModel):
    quiz_id: int
    mean_result: int


class QuizLatest(BaseModel):
    quiz_id: int
    latest: datetime

    class Config:
        orm_mode = True