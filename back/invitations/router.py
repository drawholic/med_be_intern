from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

from db.db import get_db

from sqlalchemy.ext.asyncio import AsyncSession
from users.crud import UserCrud
from .crud import InvitationsCrud
from .exceptions import SelfInvitationException
from .pd_models import Invitation

router = APIRouter(prefix='/invitations', tags=['Invitations'])

token_auth = HTTPBearer()

 
@router.get('', response_model=list[Invitation]) 
async def get_invitations(token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)):
    user_id = await UserCrud(db=db).authenticate(token=token)
    invitations = await InvitationsCrud(db=db).get_invitations(u_id=user_id)
    return invitations

 
@router.post('', status_code=status.HTTP_201_CREATED)
async def invite(c_id: int, u_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> None:
    user_id = await UserCrud(db=db).authenticate(token=token)
    
    if user_id == u_id:
        raise SelfInvitationException
    await InvitationsCrud(db=db).invite(c_id=c_id, u_id=u_id)


@router.post('/accept', status_code=status.HTTP_201_CREATED)
async def accept(inv_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> None:

    user_id = await UserCrud(db).authenticate(token)
 
    await InvitationsCrud(db=db).accept_invitation(auth_user=user_id, inv_id=inv_id)

 
@router.delete('/decline/{i_id}', status_code=status.HTTP_204_NO_CONTENT)
async def decline(i_id: int, token: str = Depends(token_auth), db: AsyncSession = Depends(get_db)) -> None:
    await UserCrud(db).authenticate(token)
    await InvitationsCrud(db=db).decline_invitation(i_id=i_id) 



