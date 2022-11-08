from pydantic import BaseModel


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