from pydantic import BaseModel
from typing import List

class UserAnswer(BaseModel):
    question_id: int
    answer_id: int


class UserQuiz(BaseModel):
    quiz_id: int
    questions: List[UserAnswer]


class UserData(BaseModel):
    quizes: List[UserQuiz]


class UserIdQuizes(BaseModel):
    id: int
    quizes: List[UserQuiz]


class UserRedisRow(BaseModel):
    id: int
    quiz_id: int
    question_id: int
    answer_id: int

