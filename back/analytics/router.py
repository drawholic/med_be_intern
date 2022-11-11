from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer

from db.db import get_db
from .crud import AnalyticsCrud
from sqlalchemy.ext.asyncio import AsyncSession
from .pd_models import (
    QuizMean,
    CompanyQuizMean,
    UserQuizMean,
    UserLatestQuizResult,
    UsersCompanyMean,
    UsersLatestQuiz,
    QuizLatest
)


from users.crud import UserCrud
from companies.crud import CompanyCrud

router = APIRouter(prefix='/analytics', tags=['Analytics'])
auth_token = HTTPBearer()


@router.get('/quiz_mean/{quiz_id}', response_model=QuizMean)
async def get_quiz_mean(quiz_id: int, db: AsyncSession = Depends(get_db)) -> QuizMean:
    return await AnalyticsCrud(db).get_quiz_mean(quiz_id=quiz_id)


@router.get('/company_quizes_mean/{company_id}', response_model=CompanyQuizMean)
async def get_company_quizes_mean(company_id: int, db: AsyncSession = Depends(get_db)) -> CompanyQuizMean:
    return await AnalyticsCrud(db).get_company_quizes_mean(company_id=company_id)


@router.get('/user_quizes_mean/{user_id}', response_model=UserQuizMean)
async def get_user_quizes_mean(user_id: int, db: AsyncSession = Depends(get_db)) -> UserQuizMean:
    return await AnalyticsCrud(db).get_user_quizes_mean(user_id=user_id)


@router.get('/user_latest_quiz/{user_id}/quiz/{quiz_id}', response_model=UserLatestQuizResult)
async def get_user_latest_quiz(user_id: int, quiz_id: int, db: AsyncSession = Depends(get_db)) -> UserLatestQuizResult:
    return await AnalyticsCrud(db).get_user_last_quiz(user_id=user_id, quiz_id=quiz_id)


@router.get('/users_mean/{company_id}', response_model=list[UsersCompanyMean])
async def company_users_quizes_mean(company_id: int, token: str = Depends(auth_token), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db).authenticate(token = token)
    if await CompanyCrud(db).is_owner(user_id=user_id, company_id=company_id) or await CompanyCrud(db).is_admin(user_id=user_id, company_id=company_id):
        return AnalyticsCrud(db).company_users_mean(company_id=company_id)


@router.get('/company/{company_id}/users/{user_id}', response_model=list[UsersCompanyMean])
async def company_user_quizes_mean(company_id:int,
                                   user_id:int,
                                   token: str = Depends(auth_token),
                                   db: AsyncSession = Depends(get_db)):
    current_user = await UserCrud(db).authenticate(token=token)
    if await CompanyCrud(db).is_owner(user_id=current_user, company_id=company_id) or await CompanyCrud(db).is_admin(user_id=current_user, company_id=company_id):
        return AnalyticsCrud(db).company_user_mean(company_id=company_id, user_id=user_id)


@router.get('/company/{company_id}/users/latest', response_model=list[UsersLatestQuiz])
async def company_users_latest_quiz(company_id: int,
                                    token: str = Depends(auth_token),
                                    db: AsyncSession = Depends(get_db)):
    curr_user = await UserCrud(db).authenticate(token=token)
    if await CompanyCrud(db).is_owner(user_id=curr_user, company_id=company_id) or await CompanyCrud(db).is_admin(user_id=curr_user, company_id=company_id):
        return AnalyticsCrud(db).users_latest_quiz(company_id=company_id)


@router.get('/users/user_id}')
async def user_quizes_mean(user_id:int,
                            token: str = Depends(auth_token),
                            db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token=token)
    return AnalyticsCrud(db).user_general_mean(user_id=user_id)


@router.get('/users/mean_list', response_model = list[UserQuizMean])
async def user_mean_list(token: str = Depends(auth_token),
                         db: AsyncSession = Depends(get_db)):
    curr_user = await UserCrud(db).authenticate(token)
    return await AnalyticsCrud(db).user_mean_list(user_id=curr_user)


@router.get('/users/latest_quizes', response_model=list[QuizLatest])
async def user_quizes_latest(token: str = Depends(auth_token),
                             db: AsyncSession = Depends(get_db)):
    curr_user = await UserCrud(db).authenticate(token=token)
    return await AnalyticsCrud(db).user_quizes_latest(user_id=curr_user)

