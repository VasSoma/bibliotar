from apiflask import APIBlueprint
from marshmallow import Schema, fields

class BookRequestSchema(Schema):
    title = fields.String()
    isbn = fields.String()
    quantity = fields.Integer()
    is_available = fields.Boolean()
    author = fields.String()

class BookResponseSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    isbn = fields.String()
    quantity = fields.Integer()
    is_available = fields.Boolean()
    author = fields.String()