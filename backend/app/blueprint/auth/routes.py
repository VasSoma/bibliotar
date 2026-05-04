from . import bp
from apiflask import HTTPError
from .schemas import LoginRequestSchema, LoginResponseSchema, RegisterRequestSchema, RegisterResponseSchema
from .services import AuthService
from .. import role_required
from ..user.schemas import RoleRequestSchema, SetRoleResponseSchema, GetRoleResponseSchema, DeleteRoleRequestSchema
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

@bp.get("/get_roles")
@bp.auth_required(auth)
@role_required(["admin"])
@bp.output(GetRoleResponseSchema(many=True))
def get_roles():
    return AuthService.get_roles()

@bp.get("/get_roles/<int:user_id>")
@bp.auth_required(auth)
@role_required(["admin"])
@bp.output(GetRoleResponseSchema(many=True))
def get_roles_by_user_id(user_id):
    return AuthService.get_roles_by_user_id(user_id)

@bp.post("/set_role")
@bp.input(RoleRequestSchema)
@bp.output(SetRoleResponseSchema)
@bp.auth_required(auth)
@role_required(["admin"])
def set_role(json_data):
    return AuthService.set_role(json_data)

@bp.delete("/delete_role")
@bp.auth_required(auth)
@role_required(["admin"])
@bp.input(DeleteRoleRequestSchema)
def delete_role(json_data):
    return AuthService.delete_role(json_data)
