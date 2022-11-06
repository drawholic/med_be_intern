from typing import Union
import json
from .pd_models import UserData, UserQuiz

EXP_HOURS = 60 * 60 * 48


class RedisCrud:
    def __init__(self, db):
        self.db = db

    async def get_user(self, user_id: int) -> Union[UserData, None]:
        user = await self.db.get(user_id)
        if user is None:
            return None
        user = json.loads(user)
        return user

    async def set_user(self, user_id: int, user_data: UserQuiz):
        user = await self.get_user(user_id=user_id)
        print(user)
        if user is None:
            user = {'quizes': {}}
        user['quizes'][user_data['quiz_id']] = user_data.get('questions')
        data = json.dumps(user)
        await self.db.set(user_id, data, EXP_HOURS)


