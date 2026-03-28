from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from backend.app.extensions import db

class Book(db.Model):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    isbn: Mapped[str] = mapped_column(String(20))
    quantity: Mapped[int] = mapped_column()
    is_available: Mapped[Optional[bool]] = mapped_column()
    author: Mapped[Optional[str]] = mapped_column(String(150))

    def __repr(self) -> str:
        return (f"Book(id={self.book_id!r},"
                f"author={self.author!r},"
                f"title={self.title!r}, "
                f"isbn={self.isbn!r},"
                f"available={self.is_available!r}")