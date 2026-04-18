from marshmallow import Schema, fields

class LoginRequestSchema(Schema):
    email = fields.String()
    password = fields.String()