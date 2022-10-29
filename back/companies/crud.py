from db.models import Company, User
from sqlalchemy import insert, select, update, join, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .pd_models import CompanyUpdate
from .exceptions import CompanyDoesNotExistException


class CompanyCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self):
        stm = select(Company).options(
            selectinload(Company.owner)
                )

        c = await self.db.execute(stm)
        c = c.scalars().all()
        return c

    async def update(self, c_id: int, company: CompanyUpdate):
        c = await self.retrieve(c_id)
        if c is None:
            raise CompanyDoesNotExistException
        stm = update(Company).where(Company.id == c_id).values(**company.dict())
        stm.execution_options(synchronize_session='fetch')

        await self.db.execute(stm)
        await self.db.commit()

    async def retrieve(self, c_id: int) -> Company:
        c = await self.db.execute(
            select(Company)
            .where(Company.id == c_id)
            .options(
                selectinload(Company.owner)
            )
        )
        c = c.scalars().first()
        return c

    async def create(self, user_id: int, company) -> Company:

        stm = insert(Company).values(title=company.title, description=company.description, owner_id=user_id)

        await self.db.execute(stm)
        await self.db.commit()

    async def delete(self, c_id: int):
        stm = delete(Company).where(Company.id == c_id)
        await self.db.execute(stm)
        await self.db.commit()
