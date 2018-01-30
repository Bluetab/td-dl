from flask import Blueprint, request, jsonify, abort
from api.common.session import get_session

session = Blueprint('session', __name__)


@session.route('/sessions', methods=['POST'])
def new_session():
    user = request.json.get('user')
    if user is None:
        abort(400, {'message': 'Missing arguments "user"'})
    username = user.get('user_name', None)
    password = user.get('password', None)
    if username is None or password is None:
        abort(400, {'message': 'Missing arguments'})
    token = get_session(username, password)
    if not token:
        return jsonify({'message': "Unauthorized"})
    return jsonify(token)
