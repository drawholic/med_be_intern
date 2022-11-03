from pydantic import BaseModel


class UserAnswer(BaseModel):
    question_id: int
    answer_id: int


class UserData(BaseModel):
    quiz_id: int
    questions: list[UserAnswer]