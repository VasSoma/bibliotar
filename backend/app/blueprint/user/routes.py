from ..user import bp
from apiflask import HTTPError
from .. import role_required
from ...extensions import auth
from .schemas import ProfileUpdateRequestSchema, ProfileUpdateResponseSchema, UserResponseSchema
from .services import UserService


@bp.get("/profile")
@bp.auth_required(auth) ### <---- Authentication need
@bp.output(UserResponseSchema)
#@role_required(["admin"]) ### <---- Only admin 
def get_profile():
    user_id = auth.current_user.get("user_id")
    success, response = UserService.get_profile(user_id)
    if success:
        return response, 200
    raise HTTPError(404, response)


@bp.patch("/profile")
@bp.auth_required(auth)
@bp.input(ProfileUpdateRequestSchema, location="json")
@bp.output(ProfileUpdateResponseSchema)
def update_profile(json_data):
    user_id = auth.current_user.get("user_id")
    success, response = UserService.update_profile(user_id, json_data)
    if success:
        return response, 200
    raise HTTPError(400, response)
