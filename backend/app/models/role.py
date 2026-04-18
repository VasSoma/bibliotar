from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from ..extensions import db
from typing import List


class Role(db.Model):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(100))

    users: Mapped[List["User"]] = relationship("User",
                                              secondary="users_roles",
                                              back_populates="roles")

    def __repr__(self) -> str:
        return f"Role id:{self.role_id}, role name:{self.role_name}"
