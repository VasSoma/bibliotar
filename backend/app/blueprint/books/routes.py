from ..books import bp

@bp.route('/books')
def books():
    return 'This is the BOOKS Blueprint'