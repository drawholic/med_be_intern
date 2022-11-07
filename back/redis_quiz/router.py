from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, StreamingResponse

from fastapi.security import HTTPBearer

from .redis_init import get_redis
from aioredis import Redis
from .crud import RedisCrud
from companies.crud import CompanyCrud
from users.crud import UserCrud
from db.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/redis', tags=['Redis'])
auth_token = HTTPBearer()


@router.get('/user_export/', response_class=FileResponse)
async def user_export(token: str = Depends(auth_token),
                      db: AsyncSession = Depends(get_db),
                      redis: Redis = Depends(get_redis)):

    current_user_id = await UserCrud(db).authenticate(token=token)
    file = await RedisCrud(redis).export_user_results(user_id=current_user_id)
    return FileResponse(file)


@router.get('/company_export/quiz/{quiz_id}')
async def company_quiz_export():
    pass


@router.get('/company_export/user/{user_id}')
async def company_user_export():
    pass


@router.get('/company_export/{company_id}')
async def company_users_export(company_id: int,
                               token: str = Depends(auth_token),
                               redis: Redis = Depends(get_redis),
                               db: AsyncSession = Depends(get_db)):

    user_id = await UserCrud(db).authenticate(token=token)

    if await CompanyCrud(db).is_owner(company_id=company_id, user_id=user_id):

        results = await CompanyCrud(db).get_users_results(company_id=company_id)
        file = await RedisCrud(redis).export_users_results(results=results,  company_id=company_id)
        return FileResponse(file)