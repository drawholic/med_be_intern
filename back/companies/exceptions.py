from fastapi import HTTPException


class CompanyDoesNotExistException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='CompanyDoesNotExist')