import functools
from datetime import datetime
from flask import current_app
from apiflask import APIBlueprint, HTTPError
from authlib.jose import jwt
from ..extensions import auth as _auth

@_auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(token.encode('ascii'), current_app.config['SECRET_KEY'])
        if data["exp"] < int(datetime.now().timestamp()):
            return None  # exp token
        return data      # auth.current_user (payload dict)
    except Exception:
        return None


def role_required(roles):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            user_roles = [r["role_name"] for r in _auth.current_user.get("roles", [])]
            if any(role in user_roles for role in roles):
                return fn(*args, **kwargs)
            raise HTTPError(403, "Access denied")
        return decorated
    return wrapper


bp = APIBlueprint('main', __name__, tag="main")

from .user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix='/user')

from .auth import bp as auth_bp
bp.register_blueprint(auth_bp, url_prefix='/auth')

from .loans import bp as loans_bp
bp.register_blueprint(loans_bp, url_prefix='/loans')

from .books import bp as books_bp
bp.register_blueprint(books_bp, url_prefix='/books')

from ..models import *
