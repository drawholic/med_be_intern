from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBearer

from db.db import get_db
from .pd_models import QuizCreate, UserResult, UserAnswers, QuestionCreate, Quiz, QuestionDetail, QuizUpdate

from .crud import QuizCrud
from users.crud import UserCrud
from redis_quiz.crud import RedisCrud
from redis_quiz.redis_init import get_redis

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/quiz', tags=['Quiz'])

auth_token = HTTPBearer()


@router.post('/user_quiz/{quiz_id}', response_model=UserResult)
async def take_quiz(quiz_id: int, answers: UserAnswers, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db), redis = Depends(get_redis)):
    user_id = await UserCrud(db=db).authenticate(token=token)
    quiz_result = await QuizCrud(db).quiz_testing(quiz_id=quiz_id, user_id=user_id, user_answers=answers)
    await RedisCrud(redis).set_user(user_id=user_id, user_data=quiz_result.redis_data)
    return {'result': quiz_result.result}


@router.get('/retrieve/{q_id}', response_model=list[QuestionDetail])
async def get_quiz(q_id: int, db: AsyncSession = Depends(get_db)):
    return await QuizCrud(db).get_quiz_detail(q_id=q_id)


@router.patch('/update/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT) 
async def update_quiz(quiz_id: int,
                      quiz_update: QuizUpdate,
                      token: str = Depends(auth_token),
                      db: AsyncSession = Depends(get_db)) -> HTTPException: 
    user_id = await UserCrud(db).authenticate(token)
    await QuizCrud(db).update_quiz(user_id=user_id, quiz_update=quiz_update, quiz_id=quiz_id)


@router.get('/list/{company_id}', response_model=list[Quiz])
async def get_quizes(company_id: int, skip: int, limit: int, db: AsyncSession = Depends(get_db)):
    return await QuizCrud(db).get_quizes(c_id=company_id, skip=skip, limit=limit)


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_quiz(quiz: QuizCreate, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)) -> HTTPException:
    user_id = await UserCrud(db).authenticate(token)
    await QuizCrud(db).create_quiz(user_id=user_id, quiz=quiz)

 
@router.post('/questions/{quiz_id}', status_code = status.HTTP_201_CREATED)
async def create_question(quiz_id: int,
                          question: QuestionCreate,
                          token: str = Depends(auth_token),
                          db: AsyncSession = Depends(get_db)) -> HTTPException: 
    await UserCrud(db).authenticate(token)
    await QuizCrud(db).create_question(quiz_id=quiz_id, question=question)


@router.delete('/quiz/{quiz_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(quiz_id: int, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)) -> HTTPException:
    curr_user = await UserCrud(db).authenticate(token)
    await QuizCrud(db).delete_quiz(user_id=curr_user, quiz_id=quiz_id)
