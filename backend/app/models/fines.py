from sqlalchemy import ForeignKey
from datetime import date
from ..extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, Boolean, Date

class Fines(db.Model):
    __tablename__ = "fines"

    fine_id : Mapped[int] = mapped_column(primary_key=True)
    amount : Mapped[int] = mapped_column(Integer)
    is_paid : Mapped[bool] = mapped_column(Boolean, default=False)
    fine_date : Mapped[date] = mapped_column(Date, default=date.today)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    loan_id: Mapped[int] = mapped_column(ForeignKey("loan.loan_id"))

    user: Mapped["User"] = relationship(back_populates="fines", lazy=True)
