from jinja2.lexer import TOKEN_DOT

from . import bp
from .schemas import BookRequestSchema
from .schemas import BookResponseSchema
from .service import BookService

@bp.get('/')
@bp.output(BookResponseSchema(many=True))
def get_books():
    return BookService.get_books()

@bp.get('/<int:book_id>')
def get_book_by_id(book_id):
    return BookService.get_book_by_id(book_id)

@bp.post('/new')
@bp.input(BookRequestSchema)
@bp.output(BookResponseSchema)
def create_book(json_data):
    return BookService.create_book(json_data)

@bp.patch('update')
@bp.input(BookRequestSchema)
@bp.output(BookResponseSchema)
def update_book(json_data):
    return BookService.update_book(json_data)

@bp.delete('/books/<int:book_id>')
def delete_book(book_id):
    return BookService.delete_book(book_id)