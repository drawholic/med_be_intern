from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from .c_models import CompanyCreate, Company
from db.db import get_db

from sqlalchemy.orm import Session

from .crud import CompanyCrud

router = APIRouter(prefix='/company', tags=['Companies'])

token_auth = HTTPBearer()

@router.post('')
async def create_company(company: CompanyCreate, token: str = HTTPBearer(), db: Session = Depends(get_db)):
    c = await CompanyCrud.create(company, db)
    return c

@router.get('')
async def list_companies(db: Session = Depends(get_db)):
    return await CompanyCrud.list(db)


@router.get('/{c_id}', response_model=Company)
async def retrieve_company(c_id: int = 1, db: Session = Depends(get_db)):
    return await CompanyCrud.retrieve(c_id, db)



