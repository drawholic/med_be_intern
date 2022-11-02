from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from db.db import get_db
from .pd_models import QuizCreate, QuestionCreate, Quiz, QuestionDetail, QuizUpdate

from .crud import QuizCrud
from users.crud import UserCrud

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/quiz', tags=['Quiz'])

auth_token = HTTPBearer()


@router.get('/retrieve/{q_id}', response_model=list[QuestionDetail])
async def get_quiz(q_id: int, db: AsyncSession = Depends(get_db)):
    return await QuizCrud(db).get_quiz_detail(q_id=q_id)


@router.patch('/update/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_quiz(quiz_id: int, quiz_update: QuizUpdate, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db).authenticate(token)
    await QuizCrud(db).update_quiz(user_id=user_id, quiz_update=quiz_update, quiz_id=quiz_id)


@router.get('/list/{company_id}', response_model=list[Quiz])
async def get_quizes(company_id: int,skip:int, limit:int, db: AsyncSession = Depends(get_db)):
    return await QuizCrud(db).get_quizes(c_id=company_id, skip=skip, limit=limit)


@router.post('/create', status_code = status.HTTP_201_CREATED)
async def create_quiz(quiz: QuizCreate, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db).authenticate(token)
    await QuizCrud(db).create_quiz(user_id=user_id, quiz=quiz)


@router.post('/questions/', status_code = status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)):
    user = await UserCrud(db).authenticate(token)
    await QuizCrud(db).create_question(user_id=user, question=question)


@router.delete('/quiz/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(quiz_id: int, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)):
    curr_user = await UserCrud(db).authenticate(token)
    await QuizCrud(db).delete_quiz(user_id=curr_user, quiz_id=quiz_id)
