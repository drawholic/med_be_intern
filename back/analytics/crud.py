from db.models import Results
from typing import List
import statistics
from sqlalchemy import select, insert, and_, desc
from .pd_models import (
    QuizMean,
    CompanyQuizMean,
    UserQuizMean,
    UserLatestQuizResult,
    UsersCompanyMean,
    UsersLatestQuiz,
    QuizLatest
)


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
        user = await self.user_latest_quiz_query(quiz_id=quiz_id, user_id=user_id)

        result = {'user_id': user_id, "last_result": float(user)}
        response = UserLatestQuizResult(**result)
        return response

    async def company_users_mean(self, company_id: int) -> List[UsersCompanyMean]:
        stm = select(Results).where(Results.company_id == company_id)
        stm = await self.db.execute(stm)
        return stm.scalars.all()

    async def company_user_mean(self, user_id: int, company_id: int) -> List[UsersCompanyMean]:
        stm = select(Results).where(and_(Results.company_id==company_id, Results.user_id==user_id))
        stm = await self.db.execute(stm)
        return stm.scalars().all()

    async def users_latest_quiz(self, company_id: int) -> List[UsersLatestQuiz]:
        stm = select(Results).where(Results.company_id == company_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        users = []

        quizes_id = set([result.quiz_id for result in results])
        users_id = set([result.user_id for result in results])

        for quiz_id in quizes_id:
            for user_id in users_id:
                users.append(await self.user_latest_quiz_query(quiz_id=quiz_id, user_id=user_id))

        return users

    async def user_latest_quiz_query(self, quiz_id: int, user_id: int):
        stm = select(Results.result).where(and_(Results.user_id == user_id, Results.quiz_id == quiz_id)).order_by(desc(Results.created_at))
        stm = await self.db.execute(stm)
        return stm.scalars().first()

    async def user_general_mean(self, user_id: int) -> UserQuizMean:
        stm = select(Results).where(Results.user_id == user_id)
        stm = await self.db.execute(stm)
        user_results = stm.scalars().all()
        results = [result.result for result in user_results]
        mean = statistics.mean(results)
        response = {'user_id': user_id, 'mean_results': mean}
        return response

    async def user_mean_list(self, user_id: int) -> List[UserQuizMean]:
        stm = select(Results).where(Results.user_id == user_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        quizes_id = set([result.quiz_id for result in results])
        mean_results = []

        for quiz_id in quizes_id:
            mean = await self.user_quiz_mean(user_id=user_id, quiz_id=quiz_id)
            mean = {'quiz_id': quiz_id, 'mean_result': mean}

            mean_results.append(UserQuizMean(**mean))

        return mean_results

    async def user_quiz_mean(self, user_id: int, quiz_id: int):
        stm = select(Results).where(and_(Results.user_id == user_id, Results.quiz_id == quiz_id))
        stm = await self.db.execute(stm)
        stm = stm.scalars().all()
        results = [result.result for result in stm]
        mean = statistics.mean(results)
        return mean

    async def user_quizes_latest(self, user_id:int) -> List[QuizLatest]:
        stm = select(Results).where(Results.user_id == user_id)
        stm = await self.db.execute(stm)
        results = stm.scalars().all()
        quizes_id = set([result.quiz_id for result in results])
        result = []

        for quiz_id in quizes_id:
            quiz = await self.get_quiz_latest_time(user_id=user_id, quiz_id=quiz_id)
            result.append(quiz)

        return result

    async def get_quiz_latest_time(self,user_id: int, quiz_id: int) -> QuizLatest:
        stm = select(Results).where(and_(Results.user_id == user_id, Results.quiz_id == quiz_id)).order_by(desc(Results.created_at))
        stm = await self.db.execute(stm)
        quiz = stm.scalars.first()
        return QuizLatest(**quiz)

