from ..loans import bp

@bp.route('/loans')
def loans():
    return 'This is the LOANS Blueprint'