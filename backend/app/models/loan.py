from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime
from typing import Optional
from ..extensions import db

class Loan(db.Model):
    __tablename__ = "loan"

    loan_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.book_id"))
    start_date: Mapped[datetime] = mapped_column(DateTime)
    due_date: Mapped[datetime] = mapped_column(DateTime)
    return_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    extension_count: Mapped[int] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="loans")
    book: Mapped["Book"] = relationship(back_populates="loans")

    def __repr__(self) -> str:
        return (f"Loan id:{self.loan_id!r},"
                f"user id:{self.user_id!r},"
                f"book_id:{self.book_id!r},"
                f"start_date:{self.start_date!r},"
                f"due_date:{self.due_date!r}")
