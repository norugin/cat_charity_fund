from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import InvestInfoAndDatesAbstractModel


class InvestmentService:
    """Сервис для работы с инвестициями.

        Этот сервис предоставляет методы для работы с инвестициями,
        включая распределение средств между проектами и обновление
        статусов инвестиций.
    """

    @staticmethod
    def get_remaining_amount(
        invested_object: InvestInfoAndDatesAbstractModel
    ) -> int:
        """Рассчитывает оставшуюся сумму для инвестирования.

        Args:
            invested_object: Инвестируемый объект

        Returns:
            Оставшаяся сумма для инвестирования
        """
        return invested_object.full_amount - invested_object.invested_amount

    @staticmethod
    def mark_as_fully_invested(
        invested_object: InvestInfoAndDatesAbstractModel
    ) -> None:
        """Закрывает инвестицию как полностью проинвестированную.

        Args:
            invested_object: Инвестируемый объект
        """
        invested_object.invested_amount = invested_object.full_amount
        invested_object.fully_invested = True
        invested_object.close_date = datetime.now()

    @staticmethod
    async def distribute_funds(
        distributed: InvestInfoAndDatesAbstractModel,
        destinations: list[InvestInfoAndDatesAbstractModel],
        session: AsyncSession
    ) -> InvestInfoAndDatesAbstractModel:
        """Распределяет инвестиционную сумму между доступными целями.

        Args:
            distributed: Распределяемый объект
            destinations: Список доступных целей
            session: Асинхронная сессия базы данных

        Returns:
            Обновленный распределяемый объект
        """
        processed_items = [distributed]
        for destination in destinations:
            processed_items.append(destination)
            distributed_remainder = (InvestmentService.
                                     get_remaining_amount(distributed))
            destination_remainder = (InvestmentService.
                                     get_remaining_amount(destination))
            if distributed_remainder <= destination_remainder:
                destination.invested_amount += distributed_remainder
                distributed.invested_amount = distributed.full_amount
                if destination.invested_amount >= destination.full_amount:
                    destination.fully_invested = True
                    destination.close_date = datetime.now()
                if distributed.invested_amount >= distributed.full_amount:
                    distributed.fully_invested = True
                    distributed.close_date = datetime.now()
                break
            else:
                destination.invested_amount = destination.full_amount
                destination.fully_invested = True
                destination.close_date = datetime.now()
                distributed.invested_amount += destination.full_amount
                if distributed.invested_amount >= distributed.full_amount:
                    distributed.fully_invested = True
                    distributed.close_date = datetime.now()
                    break

        for item in processed_items:
            session.add(item)
        await session.commit()
        for item in processed_items:
            await session.refresh(item)

        return distributed
