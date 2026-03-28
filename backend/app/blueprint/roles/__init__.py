from apiflask import APIBlueprint

bp = APIBlueprint('roles', __name__, tag='roles')

from ..roles import routes