from apiflask import APIBlueprint

bp = APIBlueprint('main',__name__,tag = "main")
@bp.route('/')
def index():
    return 'This is The Main Blueprint'


from .user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix='/user')

# from ..main import routes
from ..models import *
