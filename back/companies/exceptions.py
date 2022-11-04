from fastapi import HTTPException


class CompanyDoesNotExistException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='CompanyDoesNotExist')


class CompanyAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='Company Already Exists')


class RequestDeniedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=204, detail='Request Denied')


class RequestAccepted(HTTPException):
    def __init__(self):
        super().__init__(status_code=200, detail='Request Accepted')