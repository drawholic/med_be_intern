from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from .pd_models import CompanyCreate, Company
from db.db import get_db

from sqlalchemy.orm import Session

from .crud import CompanyCrud
from users.crud import UserCrud


router = APIRouter(prefix='/company', tags=['Companies'])

token_auth = HTTPBearer()


@router.post('')
async def create_company(company: CompanyCreate, token: str = Depends(token_auth), db: Session = Depends(get_db)):

    user = await UserCrud.authenticate(token, db)

    await CompanyCrud.create(user, company, db)


@router.get('', response_model=list[Company])
async def list_companies(db: Session = Depends(get_db)):
    return await CompanyCrud.list(db)


@router.get('/{c_id}', response_model=Company)
async def retrieve_company(c_id: int = 1, db: Session = Depends(get_db)):
    return await CompanyCrud.retrieve(c_id, db)



