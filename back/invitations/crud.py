from sqlalchemy.orm import selectinload
from sqlalchemy import insert, select, update, join, delete

from typing import Union, List
from db.models import User, Invitations, Participants, Owner
from .exceptions import AlreadyInvitedException, AuthenticationException
from companies.crud import CompanyCrud


class InvitationsCrud:

    def __init__(self, db):
        self.db = db

    async def check_invitation(self, c_id:int, u_id: int) -> Invitations:
        stm = select(Invitations).where(Invitations.company_id == c_id, Invitations.user_id == u_id)
        inv = await self.db.execute(stm)
        inv = inv.scalars().first()
        return inv

    async def get_invitations(self, u_id: int) -> List[Invitations]:
        # crud func  to get all invitations
        stm = select(Invitations).options(selectinload(Invitations.company)).where(Invitations.user_id == u_id)

        invitations = await self.db.execute(stm)
        invitations = invitations.scalars().all()

        return invitations
 
    async def accept_invitation(self,auth_user:int, inv_id: int):

        # get invitation
        stm = select(Invitations).where(Invitations.id == inv_id)
        invitation = await self.db.execute(stm)
        invitation = invitation.scalars().first()
        if not invitation.user_id == auth_user:
            raise AuthenticationException
        # creating participant
        stm = insert(Participants).values(company_id=invitation.company_id, participant_id=invitation.user_id)
        await self.db.execute(stm)

        # deleting invitation
        stm = delete(Invitations).where(Invitations.id == inv_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def decline_invitation(self, i_id: int):

        stm = delete(Invitations).where(Invitations.id == i_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def invite(self, auth_user:int, c_id: int, u_id: int):
        # creating an invitation with user and companies id`s
        stm = select(Owner).where(Owner.company_id==c_id)
        stm = await self.db.execute(stm)
        own = stm.scalars().first()

        if await self.check_invitation(c_id=c_id, u_id=u_id) is not None:
            raise AlreadyInvitedException
            #checking if authenticated user is owner of company
        if not own.user_id == auth_user:
            raise AuthenticationException

        stm = insert(Invitations).values(company_id=c_id, user_id=u_id)
        await self.db.execute(stm)
        await self.db.commit()

