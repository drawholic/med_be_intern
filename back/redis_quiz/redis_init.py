import aioredis


async def get_redis():
    async with aioredis.from_url('redis://localhost') as redis:
        yield redis