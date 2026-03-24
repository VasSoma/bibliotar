from ..extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String,Integer
from typing import List,Optional

class User(db.Model):
    __tablename__ : "users"

    user_id : Mapped[int] = mapped_column(Integer)
    role : Mapped[str] = mapped_column(String(20))
    password_hashed : Mapped[str] = mapped_column(String(255))
    phone_number : Mapped[Optional[str]] = mapped_column(String(15))
    address : Mapped[str] = mapped_column(String(100))
    name : Mapped[str]