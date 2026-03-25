from apiflask import APIBlueprint

bp = APIBlueprint('user',__name__,tag = "user")
from ..user import routes