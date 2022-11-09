from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from typing import List
from .pd_models import CompanyCreate, Company, CompanyUpdate, UserCompany, Request
from db.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CompanyCrud
from users.crud import UserCrud


router = APIRouter(prefix='/company', tags=['Companies'])

token_auth = HTTPBearer()


@router.post('', response_model=Company, status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyCreate, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> Company:
    user = await UserCrud(db=db).authenticate(token=token)
    return await CompanyCrud(db=db).create(user_id=user, company=company)


@router.get('' , response_model=List[Company])
async def list_companies(db: AsyncSession = Depends(get_db)) -> List[Company]:
    return await CompanyCrud(db=db).list()


@router.get('/requests/list/{c_id}', response_model=List[Request])
async def get_requests(company_id: int,
                       token: str = Depends(token_auth),
                       db: AsyncSession = Depends(get_db)) -> List[Request]:
    await UserCrud(db=db).authenticate(token=token)
    return await CompanyCrud(db=db).get_requests(c_id=company_id)

 
@router.post('/requests/accept', status_code=status.HTTP_201_CREATED)
async def accept_request(request_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db=db).authenticate(token=token)
    await CompanyCrud(db=db).accept_request(r_id=request_id)
    return JSONResponse(status_code=204, content={'detail': 'Request Accepted'})

 
@router.delete('/requests/decline/{request_id}', status_code=status.HTTP_204_NO_CONTENT) 
async def decline_request(request_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db=db).authenticate(token=token)
    await CompanyCrud(db=db).decline_request(r_id=request_id)
    return JSONResponse(status_code=204, content={'detail': 'Request Declined'})


@router.get('/company_detail/{c_id}', response_model=Company)
async def retrieve_company(c_id: int, db: AsyncSession = Depends(get_db)) -> Company:
    return await CompanyCrud(db=db).retrieve(c_id=c_id)


@router.patch('/update/{c_id}', response_model=Company)
async def update_company(c_id: int, company: CompanyUpdate, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> Company:
    await UserCrud(db=db).authenticate(token=token)
    await CompanyCrud(db=db).update(c_id=c_id, company=company)

    return await CompanyCrud(db=db).retrieve(c_id=c_id)


@router.delete('/delete/{c_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(c_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> HTTPException:
    await UserCrud(db=db).authenticate(token=token)
    await CompanyCrud(db=db).delete(c_id=c_id)


@router.get('/owner/{c_id}', response_model=UserCompany)
async def get_company_owner(c_id: int, db: AsyncSession = Depends(get_db)) -> UserCompany:
    return await CompanyCrud(db=db).get_owner(c_id=c_id)

