from __init__ import bp
from backend.app.blueprint.user.schemas import UserRequestSchema, UserResponseSchema
from backend.app.blueprint.user.services import UserService
from apiflask import HTTPError
from schemas import LoginRequestSchema

@bp.post("/registrate")
@bp.input(UserRequestSchema,location = "json")
@bp.output(UserResponseSchema)
def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response,status_code=400)

@bp.post("/login")
@bp.input(LoginRequestSchema,location = "json")
@bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response,status_code=400)