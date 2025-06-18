from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import CRUDDonation
from app.models import InvestInfoAndDatesAbstractModel
from app.services.investment_service import distribute_funds


async def distribute_donations(
    distributed: InvestInfoAndDatesAbstractModel,
    destinations: list[InvestInfoAndDatesAbstractModel],
    session: AsyncSession
) -> InvestInfoAndDatesAbstractModel:
    """Распределяет пожертвование между доступными проектами.

        Args:
            distributed: Распределяемый объект
            destinations: Список доступных проектов для инвестирования
            session: Асинхронная сессия базы данных

        Returns:
            Обновленный распределяемый объект с новыми данными
    """
    processed_items, distributed = await distribute_funds(distributed,
                                                          destinations)
    return await CRUDDonation.apply_distribution(processed_items,
                                                 distributed,
                                                 session)
