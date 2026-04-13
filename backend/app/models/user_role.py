from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from backend.app.extensions import db

class UserRole(db.Model):
    __tablename__ = "users_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id"), primary_key=True)