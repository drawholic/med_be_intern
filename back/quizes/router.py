from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from db.db import get_db
from .pd_models import QuizCreate, QuestionCreate, Quiz , QuizDetail

from .crud import QuizCrud
from users.crud import UserCrud

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/quiz', tags=['Quiz'])

auth_token = HTTPBearer()


@router.get('/retrieve/{q_id}', response_model=QuizDetail)
async def get_quiz(q_id: int, db: AsyncSession = Depends(get_db)):
    return await QuizCrud(db).get_quiz(q_id=q_id)


@router.get('/list/{company_id}', response_model=list[Quiz])
async def get_quizes(company_id: int, db: AsyncSession = Depends(get_db)):
    return await QuizCrud(db).get_quizes(c_id=company_id)


@router.post('/create')
async def create_quiz(quiz: QuizCreate, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db).authenticate(token)
    await QuizCrud(db).create_quiz(user_id=user_id, quiz=quiz)


@router.post('/questions/')
async def create_question(question: QuestionCreate, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)):
    user = await UserCrud(db).authenticate(token)
    await QuizCrud(db).create_question(user_id=user, question=question)