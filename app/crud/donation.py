from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User
from app.crud import CRUDBase


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self, user: User, session: AsyncSession
    ) -> list[Donation]:
        """Получение пожертвований пользователя."""
        donations = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
