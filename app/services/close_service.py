from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InvestInfoAndDatesAbstractModel


class CloseService:
    """
    Сервис для работы с закрытием проектов и пожертвований.
    """

    @staticmethod
    async def close_investment(
        investment: InvestInfoAndDatesAbstractModel,
        session: AsyncSession
    ) -> InvestInfoAndDatesAbstractModel:
        """Закрывает инвестицию как полностью проинвестированную.

        Args:
            investment: Инвестируемый объект
            session: Асинхронная сессия базы данных

        Returns:
            Обновленный инвестируемый объект
        """
        investment.fully_invested = True
        investment.close_date = datetime.utcnow()
        await session.commit()
        await session.refresh(investment)
        return investment
