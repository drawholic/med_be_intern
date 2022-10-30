from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from .pd_models import CompanyCreate, Company, CompanyUpdate, UserCompany, Request
from db.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CompanyCrud
from users.crud import UserCrud


router = APIRouter(prefix='/company', tags=['Companies'])

token_auth = HTTPBearer()


@router.post('', response_model=Company)
async def create_company(company: CompanyCreate, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> Company:
    user = await UserCrud(db).authenticate(token)
    return await CompanyCrud(db).create(user, company)


@router.get('' , response_model=list[Company])
async def list_companies(db: AsyncSession = Depends(get_db)) -> list[Company]:
    return await CompanyCrud(db).list()


@router.get('/requests/list/{c_id}', response_model = list[Request])
async def get_requests(company_id: int,
                       token: str = Depends(token_auth),
                       db: AsyncSession = Depends(get_db)) -> list[Request]:
    await UserCrud(db).authenticate(token)
    return await CompanyCrud(db).get_requests(company_id)


@router.post('/requests/accept')
async def accept_request(request_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    await CompanyCrud(db).accept_request(request_id)


@router.delete('/requests/decline/{request_id}', status_code=204)
async def decline_request(request_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    await CompanyCrud(db).decline_request(request_id)


@router.get('/company_detail/{c_id}', response_model=Company)
async def retrieve_company(c_id: int, db: AsyncSession = Depends(get_db)) -> Company:
    return await CompanyCrud(db).retrieve(c_id)


@router.patch('/update/{c_id}', response_model=Company)
async def update_company(c_id: int, company: CompanyUpdate, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> Company:
    await UserCrud(db).authenticate(token)
    await CompanyCrud(db).update(c_id, company)

    return await CompanyCrud(db).retrieve(c_id)


@router.delete('/delete/{c_id}', status_code=204)
async def delete_company(c_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    await CompanyCrud(db).delete(c_id)


@router.get('/owner/{c_id}', response_model=UserCompany)
async def get_company_owner(c_id: int, db: AsyncSession = Depends(get_db)) -> UserCompany:
    return await CompanyCrud(db).get_owner(c_id)

