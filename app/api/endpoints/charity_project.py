from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charity_project import (
    CharityProjecDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.api.validators import check_project_name_duplicate
from app.services.investment import (
    distribute_donations as donations_distribution)
from app.core.user import current_superuser
from app.api.validators import (check_project_not_fully_invested,
                                check_full_amount_not_less_than_invested)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjecDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создание нового благовторительного проекта',
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProjecDB:
    await check_project_name_duplicate(project.name, session)
    project = await charity_project_crud.create(project, session)
    project = await donations_distribution(
        distributed=project,
        destinations=await donation_crud.get_opens(session),
        session=session
    )
    return project


@router.get(
    '/',
    response_model=List[CharityProjecDB],
    response_model_exclude_none=True,
    summary='Получение списка всех благотворительных проектов',
)
async def get_charity_projects(
        session: AsyncSession = Depends(get_async_session)
) -> List[CharityProjecDB]:
    return await charity_project_crud.get_all(session)


@router.get(
    '/{project_id}',
    response_model=CharityProjecDB,
    response_model_exclude_none=True,
    summary='Получение информации о конкретном проекте',
)
async def get_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProjecDB:
    return await charity_project_crud.get_or_404(project_id, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjecDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Обновление информации о благотворительном проекте',
)
async def update_project(
        project_id: int,
        project_data: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjecDB:
    project = await charity_project_crud.get_or_404(project_id, session)
    await check_project_not_fully_invested(project_id, session)
    update_data = project_data.dict(exclude_unset=True)
    new_full_amount = update_data.get('full_amount', None)
    new_name = update_data.get('name', None)
    if new_name is not None:
        await check_project_name_duplicate(new_name, session)
    if new_full_amount is None:
        project = await charity_project_crud.update(
            project, update_data, session)
        return project
    invested_ammount = project.invested_amount
    await check_full_amount_not_less_than_invested(project_id,
                                                   new_full_amount, session)
    if new_full_amount == invested_ammount:
        project.close()
    project = await charity_project_crud.update(project, update_data, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjecDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Удаление благотовительного проекта',
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjecDB:
    project = await charity_project_crud.get_or_404(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail=f'{project} - были внесены средства, не подлежит удалению!'
        )
    project = await charity_project_crud.delete(project, session)
    return project
