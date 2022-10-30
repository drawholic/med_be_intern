from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer
from users.crud import UserCrud
from .crud import AdminCrud
from db.db import get_db

from .pd_models import Admin
from sqlalchemy.ext.asyncio import AsyncSession

router  = APIRouter(prefix='/admins', tags=['Admin'])

token_auth = HTTPBearer()


@router.get('', response_model=list[Admin])
async def get_admins(company_id: int,
                     db: AsyncSession = Depends(get_db)):
    return await AdminCrud(db).get_admins(company_id)


@router.post('/set/')
async def set_admin(user_id: int,
                    company_id: int,
                    token: str = Depends(token_auth),
                    db: AsyncSession = Depends(get_db)):

    await UserCrud(db).authenticate(token)
    await AdminCrud(db).set_admin(user_id, company_id)


@router.delete('/unset/')
async def unset_admin(user_id: int,
                      company_id: int,
                      token: str = Depends(token_auth),
                      db: AsyncSession = Depends(get_db)):

    await UserCrud(db).authenticate(token)
    await AdminCrud(db).unset_admin(user_id, company_id)
