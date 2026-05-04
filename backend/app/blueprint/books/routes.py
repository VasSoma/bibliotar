from . import bp
from .schemas import BookRequestSchema
from .schemas import BookResponseSchema
from .service import BookService
from .. import role_required
from ...extensions import auth

@bp.get('/')
@bp.output(BookResponseSchema(many=True))
def get_books():
    return BookService.get_books()

@bp.get('/<int:book_id>')
@bp.output(BookResponseSchema)
def get_book_by_id(book_id):
    return BookService.get_book_by_id(book_id)

@bp.post('/new')
@bp.input(BookRequestSchema)
@bp.output(BookResponseSchema)
@bp.auth_required(auth)
@role_required(["librarian"])
def create_book(json_data):
    return BookService.create_book(json_data)

@bp.patch('update')
@bp.input(BookRequestSchema)
@bp.output(BookResponseSchema)
@bp.auth_required(auth)
@role_required(["librarian"])
def update_book(json_data):
    return BookService.update_book(json_data)

@bp.delete('/<int:book_id>')
@bp.auth_required(auth)
@role_required(["librarian"])
def delete_book(book_id):
    return BookService.delete_book(book_id)