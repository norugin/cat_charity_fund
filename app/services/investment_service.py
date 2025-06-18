from datetime import datetime

from app.models import InvestInfoAndDatesAbstractModel


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


async def distribute_funds(
    distributed: InvestInfoAndDatesAbstractModel,
    destinations: list[InvestInfoAndDatesAbstractModel]
) -> tuple[
    list[InvestInfoAndDatesAbstractModel],
    InvestInfoAndDatesAbstractModel
]:
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
        distributed_remainder = get_remaining_amount(distributed)
        destination_remainder = get_remaining_amount(destination)
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

    return processed_items, distributed