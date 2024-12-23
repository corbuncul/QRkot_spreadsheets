from datetime import timedelta
from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        """Получение проекта по имени."""
        db_project_id = await session.execute(
            select(self.model.id).where(self.model.name == project_name)
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[dict[str, Union[str, timedelta]]]:
        """Получение списка проектов, отсортированных по скорости закрытия."""
        projects_db = await session.execute(
            select(self.model).where(self.model.fully_invested)
        )
        projects = []
        projects_db = projects_db.scalars().all()
        for project in projects_db:
            projects.append(
                {
                    'name': project.name,
                    'description': project.description,
                    'collection_time': (
                        project.close_date - project.create_date
                    )
                }
            )
        projects = sorted(
            projects, key=lambda project: project['collection_time']
        )

        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
