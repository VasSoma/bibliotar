from ..roles import bp

@bp.route('/roles')
def roles():
    return 'This is the ROLES Blueprint'