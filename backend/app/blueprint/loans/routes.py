from .. import role_required
from ..loans import bp
from apiflask import HTTPError
from ...extensions import auth
from .schemas import LoanResponseSchema, ExtendResponseSchema, ReturnResponseSchema, FinePaidResponseSchema, \
    LoanRequestSchema
from .services import LoansService


@bp.get("/history/<int:user_id>")
@bp.auth_required(auth)
@bp.output(LoanResponseSchema(many=True))
def get_history(user_id):
    requester_id = auth.current_user.get("user_id")
    requester_roles = auth.current_user.get("roles", [])

    success, response = LoansService.get_history(requester_id, requester_roles, user_id)
    if success:
        return response, 200
    raise HTTPError(403, response)


@bp.post("/history/<int:loan_id>/extend")
@bp.auth_required(auth)
@bp.output(ExtendResponseSchema)
def extend_loan(loan_id):
    requester_id = auth.current_user.get("user_id")
    requester_roles = auth.current_user.get("roles", [])

    success, response = LoansService.extend_loan(requester_id, requester_roles, loan_id)
    if success:
        return response, 200
    raise HTTPError(400, response)


@bp.post("/history/<int:loan_id>/returned")
@bp.auth_required(auth)
@bp.output(ReturnResponseSchema)
def return_loan(loan_id):
    requester_roles = auth.current_user.get("roles", [])

    success, response = LoansService.return_loan(requester_roles, loan_id)
    if success:
        return response, 200
    raise HTTPError(400, response)


@bp.post("/history/<int:loan_id>/fine_paid")
@bp.auth_required(auth)
@bp.output(FinePaidResponseSchema)
def fine_paid(loan_id):
    requester_roles = auth.current_user.get("roles", [])

    success, response = LoansService.fine_paid(requester_roles, loan_id)
    if success:
        return response, 200
    raise HTTPError(400, response)

@bp.post("history/create")
@bp.input(LoanRequestSchema)
@bp.output(LoanResponseSchema)
@bp.auth_required(auth)
@role_required(["user", "librarian"])
def create_loan(json_data):
    return LoansService.create_loan(json_data)
