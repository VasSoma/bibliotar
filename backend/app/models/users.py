from sqlalchemy import ForeignKey, Table, Column
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List, Optional

UserRole = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.user_id")),
    Column("role_id", ForeignKey("roles.role_id"))
)

UserAddress = Table(
    "users_home_address",
    Base.metadata,
    Column("user_id", ForeignKey("users.user_id")),
    Column("address_id", ForeignKey("home_address.address_id"))
)

class User(db.Model):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key=True)
    password_hashed : Mapped[str] = mapped_column(String(255))
    phone_number : Mapped[Optional[str]] = mapped_column(String(15))
    name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(255))

    addresses : Mapped[List["Home_address"]] = relationship(
        secondary=UserAddress,
        back_populates="users",
        lazy=True
    )
    roles : Mapped[List["Role"]] = relationship(secondary=UserRole, back_populates="users")
    loans : Mapped[List["Loan"]] = relationship(back_populates="user", lazy=True)
    fines : Mapped[List["Fines"]] = relationship(back_populates="user", lazy=True)

    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)
