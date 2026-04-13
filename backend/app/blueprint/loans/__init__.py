from apiflask import APIBlueprint

bp = APIBlueprint('loans', __name__, tag='loans')

from ..loans import routes