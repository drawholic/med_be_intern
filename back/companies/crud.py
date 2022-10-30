from db.models import Company, User, Owner, Invitations, Participants, Admin, Requests
from sqlalchemy import insert, select, update, join, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .pd_models import CompanyUpdate
from .exceptions import CompanyDoesNotExistException, CompanyAlreadyExists


class CompanyCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self):
        stm = select(Company).where(Company.hidden == False)
        c = await self.db.execute(stm)
        c = c.scalars().all()
        return c

    async def update(self, c_id: int, company: CompanyUpdate):
        c = await self.retrieve(c_id)
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

        return c

    async def company_title_exists(self, title):
        stm = await self.db.execute(select(Company).where(Company.title==title))
        company = stm.scalars().first()
        return bool(company)

    async def create(self, user_id: int, company) -> Company:
        if await self.company_title_exists(company.title):
            raise CompanyAlreadyExists
        stm = insert(Company).values(title=company.title, description=company.description)
        await self.db.execute(stm)

        company = await self.db.execute(select(Company).where(Company.title == company.title))
        company = company.scalars().first()
        await self.db.execute(insert(Owner).values(owner_id=user_id, company_id=company.id))
        await self.db.commit()
        return company

    async def delete(self, c_id: int):
        stm = delete(Owner).where(Owner.company_id==c_id)
        await self.db.execute(stm)
        stm = delete(Company).where(Company.id == c_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def get_owner(self, c_id: int):
        stm = select(Owner).options(selectinload(Owner.owner)).where(Owner.company_id == c_id)
        owner = await self.db.execute(stm)
        return owner.scalars().first().owner

    async def get_requests(self, c_id: int):
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
        return {'status': 'request declined'}

    async def get_participants(self, c_id: int):

        # getting participants of the company
        stm = select(Participants).options(selectinload(Participants.participant)).where(Participants.company_id == c_id)
        participants = await self.db.execute(stm)
        participants = participants.scalars().all()

        # returning just users
        return participants.participant

