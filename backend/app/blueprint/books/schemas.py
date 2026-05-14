from apiflask import APIBlueprint
from marshmallow import Schema, fields

class BookRequestSchema(Schema):
    title = fields.String(required=True)
    isbn = fields.String(required=True)
    quantity = fields.Integer(required=True)
    is_available = fields.Boolean(required=True)
    author = fields.String(required=True)

class BookResponseSchema(Schema):
    book_id = fields.Integer()
    title = fields.String()
    isbn = fields.String()
    quantity = fields.Integer()
    is_available = fields.Boolean()
    author = fields.String()

class BookQuerySchema(Schema):
    search = fields.String(load_default=None)