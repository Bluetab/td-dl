from flask_httpauth import HTTPTokenAuth
from flask import g
from api.common.session import verify_auth_token
from api.common.utils import abort

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    if not token:
        return False
    data = verify_auth_token(token)
    if data:
        g.current_user = data
        return True
    return False


@auth.error_handler
def unauthorized():
    return abort(403, {'error': 'Unauthorized access'})
