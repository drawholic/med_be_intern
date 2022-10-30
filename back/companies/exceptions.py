from fastapi import HTTPException


class CompanyDoesNotExistException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='CompanyDoesNotExist')

class CompanyAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Company Already Exists')