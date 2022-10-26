from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from db.models import Company
from db.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(prefix='/company', tags=['Companies'])


token_auth = HTTPBearer()




@router.get('')
async def list_companies(db: Session = Depends(get_db)):
    c = select(Company)
    c = await db.execute(c)
    return c.scalars().all()


@router.get('/{c_id}')
async def retrieve_company(c_id: int, db:Session = Depends(get_db)):
    pass



@router.post('')
async def create_company(company: dict, db: Session = Depends(get_db)):
    c = Company(title=company['title'],owner=2, description=company['description'])
    db.add(c)
    await db.commit()
    return c
