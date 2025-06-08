from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstracts import InvestInfoAndDatesAbstractModel


class Donation(InvestInfoAndDatesAbstractModel):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)
