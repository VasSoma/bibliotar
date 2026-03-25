from sqlalchemy import ForeignKey
from .user import UserRole

from ..APIflask.extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String,Integer
from typing import List,Optional

class Role(db.Model):
    __tablename__ = "roles"

    role_id : Mapped[int] = mapped_column(primary_key=True)
    role_name : Mapped[str] = mapped_column(String(100))

    users : Mapped[List["User"]] = relationship(secondary=UserRole, back_populates="roles")