import aioredis


async def get_redis():
    async with aioredis.from_url('redis://cache') as redis:
        yield redis