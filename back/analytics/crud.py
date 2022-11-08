from db.models import Results

import statistics
from sqlalchemy import select, insert, and_, desc
from .pd_models import QuizMean, CompanyQuizMean, UserQuizMean, UserLatestQuizResult


class AnalyticsCrud:
    def __init__(self, db):
        self.db = db

    async def get_quiz_mean(self, quiz_id: int) -> QuizMean:
        stm = select(Results.result).where(Results.quiz_id == quiz_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        mean = statistics.mean(results)
        result = {'quiz_id': quiz_id, 'mean_results': float(mean)}
        response = QuizMean(**result)
        return response

    async def get_company_quizes_mean(self, company_id: int) -> CompanyQuizMean:
        stm = select(Results.result).where(Results.company_id == company_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        mean = statistics.mean(results)
        result = {'company_id': company_id, "mean_results": float(mean)}
        response = CompanyQuizMean(**result)
        return response

    async def get_user_quizes_mean(self, user_id: int) -> UserQuizMean:
        stm = select(Results.result).where(Results.user_id == user_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        mean = statistics.mean(results)
        result = {'user_id': user_id, 'mean_results': float(mean)}
        response = UserQuizMean(**result)
        return response

    async def get_user_last_quiz(self, user_id: int, quiz_id: int) -> UserLatestQuizResult:
        stm = select(Results.result).where(and_(Results.user_id == user_id, Results.quiz_id == quiz_id)).order_by(desc(Results.created_at))
        stm = await self.db.execute(stm)
        result = stm.scalars().first()
        result = {'user_id': user_id, "last_result": float(result)}
        response = UserLatestQuizResult(**result)
        return response
