from .. import role_required
from ..loans import bp
from apiflask import HTTPError
from ...extensions import auth
from .schemas import LoanResponseSchema, LoanQuerySchema, ExtendResponseSchema, ReturnResponseSchema, FinePaidResponseSchema, \
    LoanRequestSchema
from .services import LoansService

@bp.get("")
@bp.auth_required(auth)
@bp.input(LoanQuerySchema, arg_name="query", location="query")
@bp.output(LoanResponseSchema(many=True))
def get_loans(query):
    requester_id = auth.current_user.get("user_id")
    requester_roles = auth.current_user.get("roles", [])
    success, response = LoansService.get_loans(requester_id, requester_roles, query["search"])
    if success:
        return response, 200
    raise HTTPError(400, response)

@bp.get("/<int:loan_id>")
@bp.auth_required(auth)
@bp.output(LoanResponseSchema)
def get_loan(loan_id):
    requester_id = auth.current_user.get("user_id")
    requester_roles = auth.current_user.get("roles", [])
    success, response = LoansService.get_loan(requester_id, requester_roles, loan_id)
    if success:
        return response, 200
    raise HTTPError(400, response)

@bp.post("/<int:loan_id>/extend")
@bp.auth_required(auth)
@bp.output(ExtendResponseSchema)
def extend_loan(loan_id):
    requester_id = auth.current_user.get("user_id")
    requester_roles = auth.current_user.get("roles", [])

    success, response = LoansService.extend_loan(requester_id, requester_roles, loan_id)
    if success:
        return response, 200
    raise HTTPError(400, response)


@bp.post("/<int:loan_id>/returned")
@bp.auth_required(auth)
@bp.output(ReturnResponseSchema)
def return_loan(loan_id):
    requester_roles = auth.current_user.get("roles", [])

    success, response = LoansService.return_loan(requester_roles, loan_id)
    if success:
        return response, 200
    raise HTTPError(400, response)


@bp.post("/<int:loan_id>/fine_paid")
@bp.auth_required(auth)
@bp.output(FinePaidResponseSchema)
def fine_paid(loan_id):
    requester_roles = auth.current_user.get("roles", [])

    success, response = LoansService.fine_paid(requester_roles, loan_id)
    if success:
        return response, 200
    raise HTTPError(400, response)

@bp.post("")
@bp.input(LoanRequestSchema)
@bp.output(LoanResponseSchema)
@bp.auth_required(auth)
def create_loan(json_data):
    return LoansService.create_loan(json_data)
