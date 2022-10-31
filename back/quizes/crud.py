from db.models import Quiz, Answer, Question, Owner
from .pd_models import QuizCreate, QuestionCreate, QuizDetail

from sqlalchemy import select, delete, insert, update
from sqlalchemy.orm import selectinload

from .exceptions import AuthorizationException


class QuizCrud:

    def __init__(self, db):
        self.db = db

    async def get_quiz(self, q_id: int) -> Quiz:
        stm = select(Quiz).options(selectinload(Quiz.questions)).where(Quiz.id == q_id)
        stm = await self.db.execute(stm)
        quiz = stm.scalars().first()
        return quiz

    async def get_quizes(self, c_id: int) -> list[Quiz]:
        stm = select(Quiz).where(Quiz.company_id == c_id)
        stm = await self.db.execute(stm)
        return stm.scalars().all()

    async def is_owner(self, user_id, company_id) -> bool:
        stm = select(Owner).where(Owner.company_id == company_id)
        stm = await self.db.execute(stm)
        owner = stm.scalars().first()
        return owner.owner_id == user_id

    async def create_quiz(self, user_id: int,  quiz: QuizCreate) -> None:
        if not await self.is_owner(user_id=user_id, company_id=quiz.company_id):
            raise AuthorizationException

        stm = insert(Quiz).values(**quiz.dict())

        await self.db.execute(stm)
        await self.db.commit()

    # async def add_question(self, user_id: int, quiz_id: int, question_id: int):
    #     stm = select(Quiz).options(selectinload(Quiz.questions)).where(Quiz.id == quiz_id)
    #     stm = await self.db.execute(stm)
    #     quiz = stm.scalars().first()
    #
    #     if not await self.is_owner(user_id=user_id, company_id=quiz.company_id):
    #         raise AuthorizationException
    #
    #     stm = select(Question).where(Question.id == question_id)
    #     stm = await self.db.execute(stm)
    #     question = stm.scalars().first()
    #
    #     quiz.questions.append(question)
    #
    #     await self.db.commit()

    async def create_question(self, user_id: int, question: QuestionCreate) -> None:
        quiz = await self.get_quiz(question.quiz_id)
        if not await self.is_owner(user_id=user_id, company_id=quiz.company_id):
            raise AuthorizationException

        stm = insert(Question).values(**question.dict())
        await self.db.execute(stm)
        await self.db.commit()




