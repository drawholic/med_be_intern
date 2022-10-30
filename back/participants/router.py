from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from .crud import ParticipantsCrud
from db.db import get_db
from users.crud import UserCrud

router = APIRouter(prefix='/participants', tags=['participants'])

token_auth = HTTPBearer()


@router.get('/{c_id}')
async def company_participants(c_id: int, db: AsyncSession = Depends(get_db)):
    return await ParticipantsCrud(db).company_participants(c_id)


@router.post('/request')
async def request(company_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db).authenticate(token)
    await ParticipantsCrud(db).request(company_id, user_id)


@router.get('/user_companies/{u_id}')
async def user_companies(u_id: int, db: AsyncSession = Depends(get_db)):
    return await ParticipantsCrud(db).users_companies(u_id)


@router.delete('delete_participant/')
async def delete_participant(user_id: int, company_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    await ParticipantsCrud(db).delete_participant(company_id, user_id)

