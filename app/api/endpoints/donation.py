from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDBUser,
    DonationDBSuperUser,
)
from app.services.investing import invester


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuperUser],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех пожертовований. Только для суперюзеров."""
    return await donation_crud.get_all(session)


@router.post(
    '/',
    response_model=DonationDBUser,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создание пожертвования."""
    open_projects = await charity_project_crud.get_open_objects(session)
    new_donation = await donation_crud.create(donation, session, user)
    donation, projects = invester(new_donation, open_projects)
    return await donation_crud.save_changes(donation, projects, session)


@router.get(
    '/my',
    response_model=list[DonationDBUser],
)
async def get_donations_by_user(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Список пожетрвований пользователя."""
    return await donation_crud.get_by_user(user, session)
