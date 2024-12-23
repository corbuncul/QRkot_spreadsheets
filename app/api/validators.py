from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Провверка на дублирование имени проекта"""
    project_id = await charity_project_crud.get_project_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка существования проекта"""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    return project


async def check_project_before_delete(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка проекта на возможность удаления."""
    project = await check_project_exists(project_id, session)

    if project.fully_invested or project.invested_amount or project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return project


def check_project_before_update(project: CharityProject) -> None:
    """Проверка проекта перед изменением."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект полностью проинвестирован, не подлежит изменению!',
        )


def check_project_amount(
    project: CharityProject, new_full_amount: int
) -> None:
    """Проверка нового значения "full_amount" перед изменением."""
    if project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нелья установить значение full_amount '
                'меньше уже вложенной суммы.'
            ),
        )


async def check_donation_exists(
    donation_id: int,
    session: AsyncSession,
) -> Donation:
    """Проверка существования пожертвования."""
    donation = await donation_crud.get(donation_id, session)
    if donation is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пожертвование не найдено!',
        )
    return donation
