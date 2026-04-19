from marshmallow import Schema, fields
from apiflask.validators import Email


class RoleSchema(Schema):
    role_id = fields.Integer()
    role_name = fields.String()


class PayloadSchema(Schema):
    user_id = fields.Integer()
    roles = fields.List(fields.Nested(RoleSchema))
    exp = fields.Integer()


class LoginRequestSchema(Schema):
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True)


class LoginResponseSchema(Schema):
    token = fields.String() # for test
    user_id = fields.Integer() #for test
    role = fields.String() # for test
    name = fields.String()
    email = fields.String()


class AddressRequestSchema(Schema):
    county = fields.String(required=True)
    postal_code = fields.String(required=True)
    city = fields.String(required=True)
    street = fields.String(required=True)
    house_number = fields.String(required=True)


class RegisterRequestSchema(Schema):
    email = fields.String(required=True, validate=Email())
    password = fields.String(required=True)
    name = fields.String(required=True)
    phone_number = fields.String(required=True)
    address = fields.Nested(AddressRequestSchema, required=True)


class RegisterResponseSchema(Schema):
    user_id = fields.Integer()
    role = fields.String()
    name = fields.String()
    email = fields.String()
