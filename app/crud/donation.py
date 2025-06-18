from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base_charity_repository import BaseCharityRepository
from app.models import Donation, InvestInfoAndDatesAbstractModel, User


class CRUDDonation(BaseCharityRepository[Donation]):

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> Optional[List[Donation]]:
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return user_donations.scalars().all()

    @staticmethod
    async def apply_distribution(
            processed_items: list[InvestInfoAndDatesAbstractModel],
            distributed: InvestInfoAndDatesAbstractModel,
            session: AsyncSession,
    ) -> InvestInfoAndDatesAbstractModel:
        for item in processed_items:
            session.add(item)
        await session.commit()
        for item in processed_items:
            await session.refresh(item)
        return distributed


donation_crud = CRUDDonation(Donation)
