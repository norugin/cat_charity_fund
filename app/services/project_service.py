from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_full_amount_not_less_than_invested,
                                check_project_name_duplicate,
                                check_project_not_fully_invested)
from app.crud.charity_project import CRUDCharityProject
from app.models import CharityProject


async def prepare_project_update_data(
    project: CharityProject,
    update_data: dict,
    session: AsyncSession
) -> dict:
    """Подготавливает данные для обновления проекта с проверкой условий.

        Args:
            project: Обновляемый проект
            update_data: Словарь с данными для обновления
            session: Асинхронная сессия базы данных

        Returns:
            Обновленные данные для проекта
    """
    new_full_amount = update_data.get('full_amount')
    new_name = update_data.get('name')

    if new_name is not None:
        await check_project_name_duplicate(new_name, session)

    if new_full_amount is not None:
        await check_project_not_fully_invested(project.id, session)
        await check_full_amount_not_less_than_invested(
            project.id, new_full_amount, session
        )
        if new_full_amount == project.invested_amount:
            await CRUDCharityProject(CharityProject).close(project, session)

    return update_data
