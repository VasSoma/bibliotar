from sqlalchemy import ForeignKey, Table, Column
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, Base
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship
from sqlalchemy.types import String,Integer
from typing import List,Optional

UserRole = Table( # connection table, help with user <-> user_roles.user_id <-> user_roles.roles_id <-> roles.role_id easier usage
    "users_roles",
    Base.metadata, # system get info from the base class
    Column("user_id",ForeignKey("users.user_id")),
    Column("role_id",ForeignKey("roles.role_id"))
)

class User(db.Model):
    __tablename__ = "users"

    user_id : Mapped[int] = mapped_column(primary_key=True)
    role : Mapped[str] = mapped_column(String(20))
    password_hashed : Mapped[str] = mapped_column(String(255))
    phone_number : Mapped[Optional[str]] = mapped_column(String(15))
    name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(255))

    address_id : Mapped[int] = mapped_column(ForeignKey("home_address.address_id"))
    address : Mapped["Home_address"] = relationship(back_populates="user",lazy=True) # chain request not req. bc this ; contain a class
                                                        #"user" mean in home_address.py user variable name
    roles : Mapped[List["Role"]] = relationship(secondary=UserRole,back_populates="users")

    fines : Mapped[list["Fines"]] = relationship(back_populates="user",lazy=True)


# address_email = address.user.email

    def set_password(self,password_hashed):
        self.password_hashed = generate_password_hash(password_hashed)

    def check_password(self,password_hashed):
        return check_password_hash(self.password_hashed,password_hashed)












