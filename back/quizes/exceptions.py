from fastapi import HTTPException


class AuthorizationException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Authorization Error')


class AnswersQuantityException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='There must be not less 2 or more than 6 answers')
