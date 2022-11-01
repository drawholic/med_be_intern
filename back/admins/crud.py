from sqlalchemy import select, insert, delete
from db.models import Admin
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload


class AdminCrud:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_admins(self, c_id: int) -> list[Admin]:
        stm = select(Admin).options(selectinload(Admin.user)).where(Admin.company_id == c_id)
        companies = await self.db.execute(stm)
        companies = companies.scalars().all()
        return companies

    async def set_admin(self, u_id: int, c_id: int):
        stm = insert(Admin).values(user_id=u_id, company_id=c_id)
        await self.db.execute(stm)
        await self.db.commit()

    async def unset_admin(self, u_id: int, c_id: int):
        stm = delete(Admin).where(Admin.user_id == u_id, Admin.company_id == c_id)
        await self.db.execute(stm)
        await self.db.commit()
