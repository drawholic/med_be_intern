from fastapi import HTTPException


class AuthorizationException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Authorization Error')


class AnswersQuantityException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='There must be not less than 2 answers')


class QuestionsQuantityException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='There must be not less than 2 questions')