from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from backend.app.extensions import db


class Roles(db.Model):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"Role id:{self.role_id}, role name:{self.role_name}"
