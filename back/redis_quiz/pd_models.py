from pydantic import BaseModel


class UserAnswer(BaseModel):
    question_id: int
    answer_id: int


class UserQuiz(BaseModel):
    quiz_id: int
    questions: list[UserAnswer]


class UserData(BaseModel):
    quizes: list[UserQuiz]

class UserRedisRow(BaseModel):
    id: int
    quiz_id: int
    question_id: int
    answer_id: int