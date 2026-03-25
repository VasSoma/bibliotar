from sqlalchemy import ForeignKey

from ..APIflask.extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String,Integer
from typing import List,Optional

class Home_address(db.Model):
    __tablename__ = "home_address"

    address_id : Mapped[int] = mapped_column(primary_key=True)
    country : Mapped[str] = mapped_column(String(255))
    postal_code : Mapped[str] = mapped_column(String(10))
    city : Mapped[str] = mapped_column(String(255))
    street : Mapped[str] = mapped_column(String(100))
    house_number : Mapped[str] = mapped_column(String(10))
    # user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    user: Mapped["User"] = relationship(back_populates="address",lazy=True)
                                        #"address" mean in user.py address variable name