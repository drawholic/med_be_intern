from db.models import Results

import statistics
from sqlalchemy import select, insert, and_, desc


class AnalyticsCrud:
    def __init__(self, db):
        self.db = db

    async def get_quiz_mean(self, quiz_id: int):
        stm = select(Results.result).where(Results.quiz_id == quiz_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        mean = statistics.mean(results)
        return {'quiz_id': quiz_id, 'mean_results': mean}

    async def get_company_quizes_mean(self, company_id: int):
        stm = select(Results.result).where(Results.company_id == company_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        mean = statistics.mean(results)
        return {'company_id': company_id, "mean_results": mean}

    async def get_user_quizes_mean(self, user_id: int):
        stm = select(Results.result).where(Results.user_id == user_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        mean = statistics.mean(results)
        return {'user_id': user_id, 'mean_results': mean}

    async def get_user_last_quiz(self, user_id: int, quiz_id: int):
        stm = select(Results.result).where(and_(Results.user_id == user_id, Results.quiz_id == quiz_id)).order_by(desc(Results.created_at))
        stm = await self.db.execute(stm)
        result = stm.scalars().first()
        return {'user_id': user_id, "last_result": result}
