from sqlalchemy import Column, String, Text
from datetime import datetime

from .abstracts import InvestInfoAndDatesAbstractModel


class CharityProject(InvestInfoAndDatesAbstractModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return (f'{self.name}: собрано {self.invested_amount} '
                f'из {self.full_amount}')

    def close(self):
        """Закрывает проект как полностью проинвестированный."""
        self.fully_invested = True
        self.close_date = datetime.utcnow()
