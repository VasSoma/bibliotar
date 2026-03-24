from flask import Blueprint

bp = Blueprint('main',__name__)

from backend.main import routes
from backend.models import *