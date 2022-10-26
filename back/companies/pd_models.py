from pydantic import BaseModel
from datetime import datetime





class CompanyBase(BaseModel):
    title: str
    description: str



class Company(CompanyBase):
    id: int
    create_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
