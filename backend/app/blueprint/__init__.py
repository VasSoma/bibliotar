from apiflask import APIBlueprint

bp = APIBlueprint('main',__name__,tag = "main")
@bp.route('/')
def index():
    return 'This is The Main Blueprint'


from .user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix='/user')

from .auth import bp as auth_bp
bp.register_blueprint(auth_bp, url_prefix='/auth')

from ..models import *
