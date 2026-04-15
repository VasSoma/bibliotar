from ..user import bp
@bp.route('/')
def user_index():
    return 'This is The USER Blueprint'