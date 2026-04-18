from ..user import bp

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
