from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, DateTimeAmountsMixin


class Donation(DateTimeAmountsMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return f'{self.user_id}: {self.full_amount}'
