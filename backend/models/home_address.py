from ..extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String,Integer
from typing import List,Optional

class User(db.Model):
    __tablename__ : "home_address"

    address_id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[str] = mapped_column(String(20))
    country : Mapped[str] = mapped_column(String(255))
    postal_code : Mapped[str] = mapped_column(String(10))
    city : Mapped[str] = mapped_column(String(255))
    street : Mapped[str] = mapped_column(String(100))
    house_number : Mapped[str] = mapped_column(String(10))