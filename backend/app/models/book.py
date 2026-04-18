from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db

class Book(db.Model):
    __tablename__ = "book"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    isbn: Mapped[str] = mapped_column(String(20))
    quantity: Mapped[int] = mapped_column()
    is_available: Mapped[Optional[bool]] = mapped_column()
    author: Mapped[Optional[str]] = mapped_column(String(150))

    loans: Mapped[List["Loan"]] = relationship(back_populates="book", lazy=True)

    def __repr__(self) -> str:
        return (f"Book(id={self.book_id!r},"
                f"author={self.author!r},"
                f"title={self.title!r},"
                f"isbn={self.isbn!r},"
                f"available={self.is_available!r})")
