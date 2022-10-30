from db.models import Company, User, Owner, Invitations, Participants
from sqlalchemy import insert, select, update, join, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .pd_models import CompanyUpdate
from .exceptions import CompanyDoesNotExistException

from users.crud import UserCrud


class CompanyCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self):
        stm = select(Company)
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

    async def create(self, user_id: int, company) -> Company:
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

    async def get_admins(self, c_id):
        pass

    async def get_owner(self, c_id):
        stm = select(Owner).options(selectinload(Owner.owner)).where(Owner.company_id == c_id)
        owner = await self.db.execute(stm)
        return owner.scalars().first().owner

    async def set_admin(self, c_id, u_id):
        company = await self.retrieve(c_id)
        user = await UserCrud(self.db).get_user_by_id(u_id)
        company.admins.append(user)
        await self.db.commit()
        return company

    async def get_participants(self, c_id):

        # getting participants of the company
        stm = select(Participants).options(selectinload(Participants.participant)).where(Participants.company_id == c_id)
        participants = await self.db.execute(stm)
        participants = participants.scalars().all()

        # returning just users
        return participants.participant

    async def invite(self, c_id: int, u_id: int):
        # creating an invitation with user and companies id`s
        stm = insert(Invitations).values(company_id=c_id, user_id=u_id)
        await self.db.execute(stm)
        await self.db.commit()

