from apiflask import APIBlueprint

bp = APIBlueprint('main',__name__,tag = "main")

from ..main import routes
from backend.models import *
