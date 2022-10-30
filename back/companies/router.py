from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from .pd_models import CompanyCreate, Company, CompanyUpdate, UserCompany
from db.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CompanyCrud
from users.crud import UserCrud


router = APIRouter(prefix='/company', tags=['Companies'])

token_auth = HTTPBearer()


@router.post('')
async def create_company(company: CompanyCreate, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):

    user = await UserCrud(db).authenticate(token)
    return await CompanyCrud(db).create(user, company)


@router.get(''
    # , response_model=list[Company]
            )
async def list_companies(db: AsyncSession = Depends(get_db)):
    return await CompanyCrud(db).list()


@router.get('/{c_id}'
    # , response_model=Company
            )
async def retrieve_company(c_id: int, db: AsyncSession = Depends(get_db)):
    return await CompanyCrud(db).retrieve(c_id)


@router.patch('{c_id}')
async def update_company(c_id: int, company: CompanyUpdate, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    await CompanyCrud(db).update(c_id, company)

    return await CompanyCrud(db).retrieve(c_id)


@router.delete('{c_id}', status_code=204)
async def delete_company(c_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    await CompanyCrud(db).delete(c_id)


@router.post('/invite/{c_id}')
async def invite_user(c_id: int, u_id:int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    await CompanyCrud(db).invite(c_id, u_id)


@router.get('/owner/{c_id}', response_model=UserCompany)
async def get_company_owner(c_id: int, db: AsyncSession = Depends(get_db)):
    return await CompanyCrud(db).get_owner(c_id)


@router.get('/admins/{c_id}')
async def get_company_admins(c_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    admins = await CompanyCrud(db).get_admins(c_id)
    return admins


@router.post('{c_id}/{u_id}')
async def set_admin(c_id: int, u_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    company = await CompanyCrud(db).set_admin(c_id, u_id)
    return company