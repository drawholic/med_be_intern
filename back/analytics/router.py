from fastapi import Depends, APIRouter

from db.db import get_db
from .crud import AnalyticsCrud
import aioredis
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/analytics', tags=['Analytics'])


@router.get('/quiz_mean/{quiz_id}')
async def get_quiz_mean(quiz_id: int, db: AsyncSession = Depends(get_db)):
    return await AnalyticsCrud(db).get_quiz_mean(quiz_id=quiz_id)


@router.get('/company_quizes_mean/{company_id}')
async def get_company_quizes_mean(company_id: int, db: AsyncSession = Depends(get_db)):
    return await AnalyticsCrud(db).get_company_quizes_mean(company_id=company_id)


@router.get('/user_quizes_mean/{user_id}')
async def get_user_quizes_mean(user_id: int, db: AsyncSession = Depends(get_db)):
    return await AnalyticsCrud(db).get_user_quizes_mean(user_id=user_id)


@router.get('/user_latest_quiz/{user_id}/quiz/{quiz_id}')
async def get_user_latest_quiz(user_id: int, quiz_id: int, db: AsyncSession = Depends(get_db)):
    return await AnalyticsCrud(db).get_user_last_quiz(user_id=user_id, quiz_id=quiz_id)

@router.get('/redis/hello')
async def get_redis_hello():
    return