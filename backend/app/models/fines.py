

from sqlalchemy import Boolean, ForeignKey, Table, Column
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from ..extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String,Integer, Boolean, Date
from typing import List,Optional

class Fines(db.Model):
    __tablename__ = "fines"

    fine_id : Mapped[int] = mapped_column(primary_key=True)
    amount : Mapped[int] = mapped_column(Integer)
    is_paid : Mapped[bool] = mapped_column(Boolean,default=False)
    fine_date : Mapped[date] = mapped_column(Date, default=date.today) 


    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship(back_populates="fines",lazy=True)







