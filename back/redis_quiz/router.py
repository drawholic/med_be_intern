from fastapi import APIRouter, Depends
from .redis_init import get_redis
from aioredis import Redis

router = APIRouter(prefix='/redis', tags=['Redis'])


@router.get('/user_export/{user_id}')
async def user_export(user_id: int, db: Redis = Depends(get_redis)):
    pass

