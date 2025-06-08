from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InvestInfoAndDatesAbstractModel
from app.services.investment_service import InvestmentService


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
    return await InvestmentService.distribute_funds(
        distributed, destinations, session
    )
