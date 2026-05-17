from marshmallow import Schema, fields

class LoanQuerySchema(Schema):
    search = fields.String(load_default=None)

class BookInLoanSchema(Schema):
    book_id = fields.Integer()
    title = fields.String()
    author = fields.String()

class UserInLoanSchema(Schema):
    user_id = fields.Integer()
    name = fields.String()
    email = fields.String()

class LoanRequestSchema(Schema):
    user_id = fields.Integer(load_default=None)
    user_email = fields.Email(load_default=None)
    book_id = fields.Integer(required=True)

class LoanResponseSchema(Schema):
    loan_id = fields.Integer()
    user_id = fields.Integer()
    user = fields.Nested(UserInLoanSchema, allow_none=True)
    book = fields.Nested(BookInLoanSchema)
    start_date = fields.DateTime()
    due_date = fields.DateTime()
    return_date = fields.DateTime(allow_none=True)
    extension_count = fields.Integer()
    overdue_fine = fields.Integer(allow_none=True)
    fine_is_paid = fields.Boolean(allow_none=True)


class ExtendResponseSchema(Schema):
    loan_id = fields.Integer()
    due_date = fields.DateTime()
    extension_count = fields.Integer()


class ReturnResponseSchema(Schema):
    loan_id = fields.Integer()
    return_date = fields.DateTime()


class FinePaidResponseSchema(Schema):
    fine_id = fields.Integer()
    loan_id = fields.Integer()
    amount = fields.Integer()
    is_paid = fields.Boolean()

