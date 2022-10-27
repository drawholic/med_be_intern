from db.models import Company
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class CompanyCrud:

    async def list(db: AsyncSession) -> list[Company] | list:
        c = await db.execute(select(Company))
        c = c.scalars().all()
        return c

    async def retrieve(id: int, db) -> Company:
        c = await db.execute(select(Company).where(Company.id==id))
        c = c.scalars().first()
        return c

    async def create(company, db) -> Company:
        stm = insert(Company).values(title=company.title, description=company.description, owner=1)

        await db.execute(stm)
        await db.commit()
        u = await CompanyCrud.retrieve(1, db)
        return u