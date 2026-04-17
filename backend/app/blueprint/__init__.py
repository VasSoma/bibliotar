from apiflask import APIBlueprint
from flask import render_template

bp = APIBlueprint('main', __name__, tag="main")

@bp.route('/')
def index():
    return render_template('index.html') #EZT KERESTEM 20PERCIG GYÁÁÁÁ

from .user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix='/user')

# from ..main import routes
from ..models import *