from redis_init import get_redis
from fastapi import Depends


async def get_hello(redis = Depends(get_redis)):
