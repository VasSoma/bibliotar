from ..extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List


class Home_address(db.Model):
    __tablename__ = "home_address"

    address_id : Mapped[int] = mapped_column(primary_key=True)
    county : Mapped[str] = mapped_column(String(255))
    postal_code : Mapped[str] = mapped_column(String(10))
    city : Mapped[str] = mapped_column(String(255))
    street : Mapped[str] = mapped_column(String(100))
    house_number : Mapped[str] = mapped_column(String(10))

    users: Mapped[List["User"]] = relationship(
        secondary="users_home_address",
        back_populates="addresses",
        lazy=True
    )
