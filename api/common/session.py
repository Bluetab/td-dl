import jwt
import requests

from api.app import app


URI = app.config['AUTH_SERVICE_URI']


def get_session(user, password):
    token = jwt.encode({"user_name": user, "password": password, "aud": app.config['JWT_AUD']}, app.config['SECRET_KEY'], algorithm='HS512').decode("utf-8")
    return {'token': token}

def verify_auth_token(token):
    try:
        token = jwt.decode(token, app.config['SECRET_KEY'],
                           algorithms=['HS512'],
                           audience=app.config['JWT_AUD'])
    except jwt.ExpiredSignature:
        return None
    except jwt.DecodeError:
        return None
    return token
