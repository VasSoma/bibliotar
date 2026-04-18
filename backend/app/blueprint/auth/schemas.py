from __init__ import bp
from marshmallow import Schema, fields
from apiflask.validators import Email
from apiflask import HTTPError


class LoginRequestSchema(Schema):
    email = fields.String(validate=Email)
    password = fields.String()