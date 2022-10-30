from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from db.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from users.crud import UserCrud
from .crud import InvitationsCrud
from .exceptions import SelfInvitationException
from .pd_models import Invitation

router = APIRouter(prefix='/invitations', tags=['Invitations'])

token_auth = HTTPBearer()


@router.get(''
    # , response_model=list[Invitation]
            )
async def get_invitations(token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db).authenticate(token)
    invitations = await InvitationsCrud(db).get_invitations(user_id)
    return invitations


@router.post('')
async def invite(c_id: int, u_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db).authenticate(token)
    if user_id == u_id:
        raise SelfInvitationException
    await InvitationsCrud(db).invite(c_id, u_id)


@router.post('/accept')
async def accept(i_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):

    user_id = await UserCrud(db).authenticate(token)
    invitaion = await InvitationsCrud(db).get_invitations()
    return await InvitationsCrud(db).accept_invitation(i_id)


@router.delete('/decline/{i_id}')
async def decline(i_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    await UserCrud(db).authenticate(token)
    return await InvitationsCrud(db).decline_invitation(i_id)




