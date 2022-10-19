from fastapi import HTTPException




class PasswordMismatchException(HTTPException):
    def __init__(self ):
        super().__init__(status_code=400, detail='Passwords do not match')

class UserDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='User does not exist')

class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='User already exists')
