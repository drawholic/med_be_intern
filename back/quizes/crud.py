from db.models import Quiz, Answer, Question, Owner, Admin
from .pd_models import QuizCreate, QuestionCreate, AnswerCreate, QuizUpdate

from sqlalchemy import select, delete, insert, update
from sqlalchemy.orm import selectinload

from .exceptions import AuthorizationException


class QuizCrud:

    def __init__(self, db):
        self.db = db

    async def get_quiz(self, q_id: int):

        stm = select(Question).options(selectinload(Question.answers)).where(Question.quiz_id == q_id)
        stm = await self.db.execute(stm)
        quiz = stm.scalars().all()
        return quiz



    async def get_quizes(self, c_id: int, skip:int, limit: int) -> list[Quiz]:
        stm = select(Quiz).options(selectinload(Quiz.questions)).where(Quiz.company_id == c_id).offset(skip).limit(limit)
        stm = await self.db.execute(stm)
        quizes = stm.scalars().all()
        return quizes

    async def is_admin(self, user_id: int, company_id: int) -> bool:
        stm = select(Admin).where(Admin.company_id == company_id)
        stm = await self.db.execute(stm)
        companies = stm.scalars().all()
        admin = None
        for company in companies:
            if company.user_id == user_id:
                admin = True
        return bool(admin)

    async def is_owner(self, user_id, company_id) -> bool:
        stm = select(Owner).where(Owner.company_id == company_id)
        stm = await self.db.execute(stm)
        owner = stm.scalars().first()
        return owner.owner_id == user_id

    async def create_answer(self, question_id: int, answer: AnswerCreate) -> None:
        stm = insert(Answer).values(**answer, question_id=question_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def create_question(self, quiz_id: int, question: QuestionCreate) -> None:
        answers = question.pop('answers')

        stm = insert(Question).returning(Question.id).values(quiz_id=quiz_id, **question)
        stm = await self.db.execute(stm)

        await self.db.commit()

        question_id = stm.fetchone()[0]
        for answer in answers:
            await self.create_answer(question_id=question_id, answer=answer)
            await self.db.commit()

    async def create_quiz(self, user_id: int,  quiz: QuizCreate):
        if not await self.is_owner(user_id=user_id, company_id=quiz.company_id) or await self.is_admin(user_id=user_id, company_id=quiz.company_id):
            raise AuthorizationException
        quiz = quiz.dict()
        questions = quiz.pop('questions')

        stm = insert(Quiz).returning(Quiz).values(**quiz)
        quiz = await self.db.execute(stm)
        quiz_id = quiz.fetchone()[0]
        for question in questions:
            await self.create_question(quiz_id=quiz_id, question=question)

    async def update_quiz(self, user_id: int, quiz_id:int, quiz_update: QuizUpdate):
        quiz = await self.get_quiz(q_id=quiz_id)
        if not await self.is_admin(user_id=user_id, company_id=quiz.company_id) or await self.is_owner(user_id=user_id, company_id=quiz.company_id):
            raise AuthorizationException
        stm = update(Quiz).values(**quiz_update.dict(exclude_unset=True)).where(Quiz.id == quiz_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def delete_quiz(self, user_id: int, quiz_id: int):
        quiz = await self.get_quiz(q_id=quiz_id)
        if not await self.is_owner(user_id=user_id, company_id=quiz.company_id) or await self.is_admin(user_id=user_id, company_id=quiz.company_id):
            raise AuthorizationException

    async def delete_questions(self, quiz_id: int):
        stm = select(Question).where(Question.quiz_id == quiz_id)
        stm = await self.db.execute(stm)
        questions = stm.scalars().all()

        for question in questions:
            await self.delete_answers(question_id=question.id)

        stm = delete(Question).where(Question.quiz_id == quiz_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def delete_answers(self, question_id: int):
        stm = delete(Answer).where(Answer.question_id == question_id)
        await self.db.execute(stm)
        await self.db.commit()
