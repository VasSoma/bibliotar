from apiflask import APIBlueprint

bp = APIBlueprint('books', __name__, tag='books')

from ..books import routes