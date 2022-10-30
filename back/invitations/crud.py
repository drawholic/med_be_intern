from sqlalchemy.orm import selectinload
from sqlalchemy import insert, select, update, join, delete

from db.models import User, Invitations, Participants
from .exceptions import AlreadyInvitedException


class InvitationsCrud:

    def __init__(self, db):
        self.db = db

    async def check_invitation(self, c_id:int, u_id: int):
        stm = select(Invitations).where(Invitations.company_id == c_id, Invitations.user_id == u_id)
        inv = await self.db.execute(stm)
        inv = inv.scalars().first()
        return inv

    async def get_invitations(self, u_id: int):
        # crud func  to get all invitations
        stm = select(Invitations).options(selectinload(Invitations.company)).where(Invitations.user_id == u_id)

        invitations = await self.db.execute(stm)
        invitations = invitations.scalars().all()

        return invitations

    async def accept_invitation(self, i_id: int):

        # get invitation
        stm = select(Invitations).where(Invitations.id == i_id)
        invitation = await self.db.execute(stm)
        invitation = invitation.scalars().first()

        # creating participant
        stm = insert(Participants).values(company_id=invitation.company_id, participant_id=invitation.user_id)
        await self.db.execute(stm)

        # deleting invitation
        stm = delete(Invitations).where(Invitations.id == i_id)
        await self.db.execute(stm)
        await self.db.commit()
        return {'status': 'invitation accepted'}

    async def decline_invitation(self, i_id: int):

        stm = delete(Invitations).where(Invitations.id == i_id)
        await self.db.execute(stm)
        await self.db.commit()
        return {'status': 'Invitation declined'}

    async def invite(self, c_id: int, u_id: int):
        # creating an invitation with user and companies id`s
        if await self.check_invitation(c_id, u_id) is not None:
            raise AlreadyInvitedException
        stm = insert(Invitations).values(company_id=c_id, user_id=u_id)
        await self.db.execute(stm)
        await self.db.commit()

