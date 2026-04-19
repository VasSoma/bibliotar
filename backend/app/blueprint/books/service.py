from apiflask import HTTPError

from ...models.book import Book
from ...extensions import db

class BookService:

    @staticmethod
    def get_books():
        books = Book.query.all()
        if not books:
            raise HTTPError(message="No books available", status_code=404)
        return books

    @staticmethod
    def get_book_by_id(book_id):
        book = Book.query.get(book_id)
        if not book:
            raise HTTPError(message="There is no book with this ID", status_code=404)
        return book

    @staticmethod
    def create_book(json_data):
        book = Book(
            title=json_data["title"],
            isbn=json_data["isbn"],
            quantity=json_data["quantity"],
            is_available=json_data.get("is_available", True),
            author=json_data["author"]
        )

        db.session.add(book)
        db.session.commit()

        return book

    @staticmethod
    def update_book(json_data):
        book = Book.query.where(json_data["isbn"] == Book.isbn).first()

        if not book:
            raise HTTPError(404, "Book not found")

        for key, value in json_data.items():
            setattr(book, key, value)

        db.session.commit()

        return book

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            raise HTTPError(404, "Book not found")
        else:
            db.session.delete(book)
            db.session.commit()

        return "", 204


