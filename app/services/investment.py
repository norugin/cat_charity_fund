from sqlalchemy.ext.asyncio import AsyncSession
from app.models import InvestInfoAndDatesAbstractModel
from app.services.investment_service import InvestmentService


async def distribute_donations(
    distributed: InvestInfoAndDatesAbstractModel,
    destinations: list[InvestInfoAndDatesAbstractModel],
    session: AsyncSession
) -> InvestInfoAndDatesAbstractModel:
    """
    Распределяет пожертвование между доступными проектами.
    """
    return await InvestmentService.distribute_funds(
        distributed, destinations, session
    )
