from apiflask import APIBlueprint
from flask import render_template

bp = APIBlueprint('main', __name__, tag="main")

@bp.route('/')
def index():
    return render_template('index.html')

# from ..main import routes
from backend.models import *