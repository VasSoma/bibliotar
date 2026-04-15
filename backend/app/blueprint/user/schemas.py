from marshmallow import Schema,fields
from apiflask.validators import Email

class AddressSchema(Schema):
    city = fields.String()
    street = fields.String()
    country = fields.String()
    postal_code = fields.String()
    house_number = fields.String()



class UserRequestSchema(Schema):
    password_hashed = fields.String()
    phone_number = fields.String()
    name = fields.String()
    email = fields.String(validate=Email())
    address = fields.Nested(AddressSchema)

class UserResponseSchema(Schema): #API response
    id = fields.Integer()
    role = fields.String()
    phone_number = fields.String()
    name = fields.String()
    email = fields.String(validate=Email)
    address = fields.Nested(AddressSchema)

class UserLoginSchema(Schema):
    email = fields.String(validate=Email)
    password = fields.String()
