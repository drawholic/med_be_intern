from fastapi import HTTPException


class AlreadyInvitedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail='User already invited')


class SelfInvitationException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="You can't invite yourself")


class AuthenticationException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Authentication error")
