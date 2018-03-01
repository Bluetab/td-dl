import jwt
import requests

from api.app import app


URI = app.config['AUTH_SERVICE_URI']


def get_session(user, password):
    resp = requests.post(URI, json={"user": {"user_name": user,
                                    "password": password}})
    if not resp.status_code == 201:
        return None
    return resp.json()


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
