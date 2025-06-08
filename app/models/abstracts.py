from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class InvestInfoAndDatesAbstractModel(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='full_amount_check'),
        CheckConstraint('invested_amount >= 0', name='invested_amount_check'),
        CheckConstraint('full_amount >= invested_amount',
                        name='amounts_check'),
    )

    full_amount = Column(Integer, nullable=False, default=0)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime, nullable=True)
