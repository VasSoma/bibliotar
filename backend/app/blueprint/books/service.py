from apiflask import HTTPError

from ...models.book import Book
from ...extensions import db

class BookService:

    @staticmethod
    def get_books(search=None):
        query = Book.query
        if search:
            like = f"%{search}%"
            query = query.filter(
                db.or_(Book.title.ilike(like), Book.author.ilike(like))
            )
        books = query.all()
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
        book = Book.query.where(json_data["isbn"] == Book.isbn).first()
        if not book:
            raise HTTPError(409, "Book already exists with same ISBN.")

        try:
            new_book = Book(
                title=json_data["title"],
                isbn=json_data["isbn"],
                quantity=json_data["quantity"],
                is_available=json_data.get("is_available", True),
                author=json_data["author"],
            )

            db.session.add(new_book)
            db.session.commit()
        except Exception:
            raise HTTPError(500, "Failed to create new book.")

        return new_book

    @staticmethod
    def update_book(json_data, book_id):
        book = Book.query.where(book_id == Book.book_id).first()

        if not book:
            raise HTTPError(404, "Book not found")

        # NOTE: ha nincs try except block akkor unhandled lesz az error
        # sima 500 internal server error megy vissza responsekent
        try:
            for key, value in json_data.items():
                setattr(book, key, value)

            # NOTE: innen johet error
            db.session.commit()

            return book
        except Exception:
            raise HTTPError(500, "Failed to update book.")

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            raise HTTPError(404, "Book not found")

        try:
            db.session.delete(book)
            db.session.commit()
            return "", 204
        except:
            raise HTTPError(500, "Failed to delete book.")




