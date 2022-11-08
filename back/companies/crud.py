from db.models import Company, User, Owner, Invitations, Participants, Admin, Requests, Results
from sqlalchemy import insert, select, update, join, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


from .pd_models import CompanyUpdate
from .exceptions import CompanyDoesNotExistException, CompanyAlreadyExists
from typing import List


class CompanyCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self) -> Company:
        stm = select(Company).where(Company.hidden == False)
        c = await self.db.execute(stm)
        c = c.scalars().all()
        return c
 
    async def update(self, c_id: int, company: CompanyUpdate):
        c = await self.retrieve(c_id=c_id)
        if c is None:
            raise CompanyDoesNotExistException
        stm = update(Company).where(Company.id == c_id).values(**company.dict(exclude_unset=True))
        stm.execution_options(synchronize_session='fetch')

        await self.db.execute(stm)
        await self.db.commit()

    async def retrieve(self, c_id: int) -> Company:
        c = await self.db.execute(
            select(Company)
            .where(Company.id == c_id)
            )

        c = c.scalars().first()
        if c is None:
            raise CompanyDoesNotExistException

    async def company_title_exists(self, title: str) -> bool: 
        stm = await self.db.execute(select(Company).where(Company.title==title)) 
        company = stm.scalars().first()
        return bool(company)

    async def create(self, user_id: int, company) -> Company:
        if await self.company_title_exists(title=company.title):
            raise CompanyAlreadyExists
        stm = insert(Company).values(title=company.title, description=company.description)
        await self.db.execute(stm)

        company = await self.db.execute(select(Company).where(Company.title == company.title))
        company = company.scalars().first()
        await self.db.execute(insert(Owner).values(owner_id=user_id, company_id=company.id))
        await self.db.commit()
        return company

    async def delete(self, c_id: int):
        stm = delete(Owner).where(Owner.company_id == c_id) 
        await self.db.execute(stm)

        stm = delete(Company).where(Company.id == c_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def get_owner(self, c_id: int) -> User:
        stm = select(Owner).options(selectinload(Owner.owner)).where(Owner.company_id == c_id)
        owner = await self.db.execute(stm)
        return owner.scalars().first().owner

    async def is_owner(self, user_id: int, company_id: int) -> bool:
        stm = select(Owner).where(and_(Owner.company_id==company_id, Owner.owner_id == user_id))
        stm = await self.db.execute(stm)
        return bool(stm.scalars().first())

    async def is_admin(self, user_id: int, company_id: int) -> bool:
        stm = select(Admin).where(and_(Admin.user_id==user_id, Admin.company_id == company_id))
        stm = await self.db.execute(stm)
        return bool(stm.scalars().first())

    async def get_requests(self, c_id: int) -> List[Requests]:
        stm = select(Requests).options(selectinload(Requests.user)).where(Requests.company_id == c_id)
        stm = await self.db.execute(stm)
        requests = stm.scalars().all()
        return requests

    async def accept_request(self, r_id: int):
        stm = select(Requests).where(Requests.id == r_id )
        stm = await self.db.execute(stm)
        request = stm.scalars().first()

        stm = insert(Participants).values(company_id=request.company_id, participant_id=request.user_id)
        await self.db.execute(stm)
        stm = delete(Requests).where(Requests.id == request.id)
        await self.db.execute(stm)
        await self.db.commit()

    async def decline_request(self, r_id: int):
        stm = delete(Requests).where(Requests.id == r_id)
        await self.db.execute(stm)

    async def get_participants(self, c_id: int) -> List[User]:

        # getting participants of the company
        stm = select(Participants).options(selectinload(Participants.participant)).where(Participants.company_id == c_id)
        participants = await self.db.execute(stm)
        participants = participants.scalars().all()

        # returning just users
        return participants.participant

    async def get_users_results(self, company_id: int) -> List[Results]:
        stm = select(Results).where(Results.company_id == company_id)
        stm = await self.db.execute(stm)
        return stm.scalars().all()

    async def get_quiz_results(self, quiz_id: int) -> List[Results]:
        stm = select(Results).where(Results.quiz_id == quiz_id)
        stm = await self.db.execute(stm)
        return stm.scalars().all()