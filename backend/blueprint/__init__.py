from apiflask import APIBlueprint

bp = APIBlueprint('main',__name__,tag = "main")
@bp.route('/')
def index():
    return 'This is The Main Blueprint'

# from ..main import routes
from backend.models import *
