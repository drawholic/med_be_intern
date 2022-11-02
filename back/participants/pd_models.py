from pydantic import BaseModel
from companies.pd_models import Company
from users.pd_models import User


class ParticipantCompany(BaseModel):
    company: Company

    class Config:
        orm_mode = True


class ParticipantUser(BaseModel):
    participant: User

    class Config:
        orm_mode = True
