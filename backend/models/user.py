

from sqlalchemy import ForeignKey

from ..extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String,Integer
from typing import List,Optional

class User(db.Model):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key=True)
    role : Mapped[str] = mapped_column(String(20))
    password_hashed : Mapped[str] = mapped_column(String(255))
    phone_number : Mapped[Optional[str]] = mapped_column(String(15))
    name : Mapped[str] = mapped_column(String(100)) 

    address_id : Mapped[int] = mapped_column(ForeignKey("home_address.address_id"))