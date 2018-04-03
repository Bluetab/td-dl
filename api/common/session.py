import jwt
from api.app import app


def verify_auth_token(token):
    try:
        token = jwt.decode(token, app.config['SECRET_KEY'],
                           algorithms=app.config['ALGORITHM'],
                           audience=app.config['JWT_AUD'])
    except jwt.ExpiredSignature:
        return None
    except jwt.DecodeError:
        return None
    return token
