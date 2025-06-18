from http import HTTPStatus

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession
) -> None:
    """
    Проверяет уникальность имени проекта.
    """
    project_id = await charity_project_crud.get_id_by_name(name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Проект с именем \'{name}\' уже существует.'
        )


async def check_project_not_fully_invested(
        project_id: int,
        session: AsyncSession
) -> None:
    """
    Проверяет, что проект не полностью проинвестирован.
    """
    project = await charity_project_crud.get_or_404(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Проект {project.name} закрыт, редактирование недоступно!'
        )


async def check_full_amount_not_less_than_invested(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession
) -> None:
    """
    Проверяет, что новая сумма не меньше уже вложенной.
    """
    project = await charity_project_crud.get_or_404(project_id, session)
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Нельзя установить значение full_amount'
                   f' меньше уже вложенной суммы: {project.invested_amount}.'
        )


async def check_is_project_invested(
        project: CharityProject
) -> None:
    """
    Проверяет, есть ли инвестиции в проект, перед его удалением.
    """
    if project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail=f'{project} - были внесены средства, не подлежит удалению!'
        )
