from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

NAME_MAX_LENGHT = 100


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=NAME_MAX_LENGHT)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        orm_mode = True
        extra = Extra.forbid


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=NAME_MAX_LENGHT)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        orm_mode = True
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    create_date: datetime = Field(default_factory=datetime.now)
    close_date: Optional[datetime]
    fully_invested: Optional[bool] = False
    invested_amount: int = 0


class CharityProjectInvested(BaseModel):
    name: str
    description: str
    collection_time: timedelta

    class Config:
        json_encoders = {timedelta: str}
