from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import ParticipantsCrud
from db.db import get_db
from db.models import Participants

from users.crud import UserCrud
from .pd_models import ParticipantUser, ParticipantCompany

router = APIRouter(prefix='/participants', tags=['participants'])

token_auth = HTTPBearer()


@router.get('/{c_id}', response_model=list[ParticipantUser])
async def company_participants(c_id: int, db: AsyncSession = Depends(get_db)) -> list[Participants]:
    return await ParticipantsCrud(db=db).company_participants(c_id=c_id)


@router.post('/request')
async def request(company_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> None:
    user_id = await UserCrud(db=db).authenticate(token=token)
    await ParticipantsCrud(db=db).request(c_id=company_id, u_id=user_id)


@router.get('/user_companies/{u_id}', response_model=list[ParticipantCompany])
async def user_companies(u_id: int, db: AsyncSession = Depends(get_db)) -> list[Participants]:
    return await ParticipantsCrud(db=db).users_companies(u_id=u_id)


@router.delete('delete_participant/', status_code=204)
async def delete_participant(user_id: int, company_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> None:
    await UserCrud(db=db).authenticate(token=token)
    await ParticipantsCrud(db=db).delete_participant(c_id=company_id, u_id=user_id)

