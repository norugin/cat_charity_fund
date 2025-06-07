from datetime import datetime

from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import CharityProject, Donation
from app.crud.base_repository import BaseRepository

T = TypeVar('T', CharityProject, Donation)


class BaseCharityRepository(BaseRepository[T]):
    def __init__(self, model):
        super().__init__(model)

    async def get_opens(
            self,
            session: AsyncSession
    ) -> list[T]:
        objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            ).order_by(self.model.create_date)
        )
        return objects.scalars().all()

    async def close(
            self,
            db_object: T,
            session: AsyncSession
    ) -> T:
        db_object.fully_invested = True
        db_object.close_date = datetime.utcnow()
        return await self.save(db_object, session)
