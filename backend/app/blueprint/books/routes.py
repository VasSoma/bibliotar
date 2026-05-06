from . import bp
from .schemas import BookRequestSchema
from .schemas import BookResponseSchema
from .schemas import BookQuerySchema
from .service import BookService
from .. import role_required
from ...extensions import auth

@bp.get('')
@bp.input(BookQuerySchema, arg_name="query", location="query")
@bp.output(BookResponseSchema(many=True))
def get_books(query):
    return BookService.get_books(query["search"])

@bp.get('/<int:book_id>')
@bp.output(BookResponseSchema)
def get_book_by_id(book_id):
    return BookService.get_book_by_id(book_id)

@bp.post('')
@bp.input(BookRequestSchema)
@bp.output(BookResponseSchema)
@bp.auth_required(auth)
@role_required(["admin"])
def create_book(json_data):
    return BookService.create_book(json_data)

@bp.patch('/<int:book_id>')
@bp.input(BookRequestSchema)
@bp.output(BookResponseSchema)
@bp.auth_required(auth)
@role_required(["admin"])
def update_book(json_data):
    return BookService.update_book(json_data)

@bp.delete('/<int:book_id>')
@bp.auth_required(auth)
@role_required(["admin"])
def delete_book(book_id):
    return BookService.delete_book(book_id)