from marshmallow import Schema, fields


class AddressSchema(Schema):
    county = fields.String()
    postal_code = fields.String()
    city = fields.String()
    street = fields.String()
    house_number = fields.String()


class UserResponseSchema(Schema):
    user_id = fields.Integer()
    role = fields.String()
    name = fields.String()
    email = fields.String()
    phone_number = fields.String()
    address = fields.Nested(AddressSchema)


class ProfileUpdateRequestSchema(Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone_number = fields.String(required=True)
    address = fields.Nested(AddressSchema, required=True)


class ProfileUpdateResponseSchema(Schema):
    name = fields.String()
    email = fields.String()
    phone_number = fields.String()
    address = fields.Nested(AddressSchema)

class RoleResponseSchema(Schema):
    role_id = fields.Integer()
    role_name = fields.String()
