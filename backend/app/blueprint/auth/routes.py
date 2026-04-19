from . import bp
from apiflask import HTTPError
from .schemas import LoginRequestSchema, LoginResponseSchema, RegisterRequestSchema, RegisterResponseSchema
from .services import AuthService
from ...extensions import auth


@bp.post("/login")
@bp.input(LoginRequestSchema, location="json")
@bp.output(LoginResponseSchema)
def login(json_data):
    success, response = AuthService.login(json_data)
    if success:
        return response, 200
    raise HTTPError(status_code=401, message=response)


@bp.post("/register")
@bp.input(RegisterRequestSchema, location="json")
@bp.output(RegisterResponseSchema, status_code=201)
def register(json_data):
    success, response = AuthService.register(json_data)
    if success:
        return response, 201
    raise HTTPError(status_code=400, message=response)


@bp.post("/logout")
@bp.auth_required(auth)
@bp.output({}, status_code=200)
def logout():
    return {}, 200
