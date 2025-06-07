from sqlalchemy import Column, Text, ForeignKey, Integer
from datetime import datetime

from .abstracts import InvestInfoAndDatesAbstractModel


class Donation(InvestInfoAndDatesAbstractModel):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)

    def close(self):
        """Закрывает пожертвование как полностью проинвестированное."""
        self.fully_invested = True
        self.close_date = datetime.utcnow()
