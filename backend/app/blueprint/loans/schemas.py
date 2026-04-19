from marshmallow import Schema, fields


class BookInLoanSchema(Schema):
    book_id = fields.Integer()
    title = fields.String()
    author = fields.String()


class LoanResponseSchema(Schema):
    loan_id = fields.Integer()
    user_id = fields.Integer()
    book = fields.Nested(BookInLoanSchema)
    start_date = fields.DateTime()
    due_date = fields.DateTime()
    extension_count = fields.Integer()


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
