from .schemas import UserLoginSchema, UserRequestSchema, UserResponseSchema
from .services import UserService
from ..user import bp
from apiflask import HTTPError



# @bp.output(UserResponseSchema(many=True)) #if the answer is a list

# @bp.input(UserRequestSchema,location = "query")
# def user_registrate(query_data):
#     pass

# @bp.post("/registrate=<int:id>")
# def user_registrate(data,id):
#     pass



@bp.route('/')
def user_index():
    return 'This is The USER Blueprint'

@bp.post("/registrate")
@bp.input(UserRequestSchema,location = "json")
@bp.output(UserResponseSchema)


def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response,status_code=400)



@bp.post("/login")
@bp.input(UserLoginSchema,location = "json")
@bp.output(UserResponseSchema)


def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response,status_code=400)

