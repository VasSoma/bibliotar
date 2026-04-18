from marshmallow import Schema, fields
from apiflask.validators import Email

class LoginRequestSchema(Schema):
    email = fields.String(validate=Email)
    password = fields.String()