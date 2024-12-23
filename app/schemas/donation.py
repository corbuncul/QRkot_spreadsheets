from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        orm_mode = True
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDBUser(DonationBase):
    id: int
    create_date: datetime


class DonationDBSuperUser(DonationDBUser):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
