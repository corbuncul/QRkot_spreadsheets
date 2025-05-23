from datetime import timedelta
from typing import Union

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)
from app.schemas.charity_project import CharityProjectInvested

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectInvested],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
) -> list[dict[str, Union[str, timedelta]]]:
    """Только для суперюзеров. Топ проектов по скорости закрытия."""
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid, projects, wrapper_services)
    return projects
