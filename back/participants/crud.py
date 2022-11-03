from db.models import Participants, Requests, Company, User
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload


class ParticipantsCrud:
    def __init__(self, db):
        self.db = db

    async def request(self, c_id: int, u_id: int):
        stm = insert(Requests).values(user_id=u_id, company_id=c_id)
        await self.db.execute(stm)
        await self.db.commit()
 
    async def company_participants(self, c_id: int) -> list[Participants]: 
        stm = select(Participants).options(selectinload(Participants.participant)).where(Participants.company_id == c_id)
        users = await self.db.execute(stm)
        users = users.scalars().all()
        return users
 
    async def users_companies(self, u_id: int) -> list[Participants]: 
        stm = select(Participants).options(selectinload(Participants.company)).where(Participants.participant_id == u_id)
        companies = await self.db.execute(stm)
        companies = companies.scalars().all()
        return companies

    async def delete_participant(self, c_id: int, u_id: int):
        stm = delete(Participants).where(Participants.company_id==c_id, Participants.participant_id==u_id) 
        await self.db.execute(stm)
        await self.db.commit()
