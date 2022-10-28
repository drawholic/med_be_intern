from db.models import Company, User
from sqlalchemy import insert, select, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class CompanyCrud:

    async def list(db: AsyncSession):
        stm = select(Company).options(
            selectinload(Company.owner)
                )

        c = await db.execute(stm)
        c = c.scalars().all()
        return c

    async def retrieve(id: int, db) -> Company:
        c = await db.execute(
            select(Company)
            .where(Company.id==id)
            .options(
                selectinload(Company.owner)
            )
        )
        c = c.scalars().first()
        return c

    async def create(user: int, company, db) -> Company:

        stm = insert(Company).values(title=company.title, description=company.description, owner_id=user)

        await db.execute(stm)
        await db.commit()

