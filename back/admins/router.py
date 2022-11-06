from fastapi import Depends, APIRouter, status, HTTPException
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
    return await AdminCrud(db=db).get_admins(c_id=company_id)


@router.post('/set/', status_code=status.HTTP_204_NO_CONTENT)
async def set_admin(user_id: int,
                    company_id: int,
                    token: str = Depends(token_auth),
                    db: AsyncSession = Depends(get_db)) -> HTTPException:

    await UserCrud(db=db).authenticate(token=token)
    await AdminCrud(db=db).set_admin(u_id=user_id, c_id=company_id)


@router.delete('/unset/', status_code=status.HTTP_204_NO_CONTENT)
async def unset_admin(user_id: int,
                      company_id: int,
                      token: str = Depends(token_auth),
                      db: AsyncSession = Depends(get_db)) -> HTTPException:

    await UserCrud(db=db).authenticate(token=token)
    await AdminCrud(db=db).unset_admin(u_id=user_id, c_id=company_id)
