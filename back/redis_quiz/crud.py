from .redis_init import get_redis
import json
from .pd_models import UserData

EXP_HOURS = 60 * 60 * 48


class RedisCrud:
    def __init__(self, db):
        self.db = db

    async def get_user(self, user_id: int) -> UserData:
        user = await self.db.get(user_id)
        user = json.loads(user)
        return user

    async def set_user(self, user_id: int, user_data: dict):
        data = json.dumps(user_data)
        await self.db.set(user_id, data, EXP_HOURS)


