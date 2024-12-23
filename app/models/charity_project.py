from sqlalchemy import Column, String, Text

from app.core.db import Base, DateTimeAmountsMixin

NAME_MAX_LENGHT = 100


class CharityProject(DateTimeAmountsMixin, Base):
    name = Column(String(NAME_MAX_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'{self.name}: {self.full_amount}'
