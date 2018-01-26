from flask import Blueprint, request, jsonify, abort, url_for, g
from api.settings.db import db
from api.settings.auth import auth
from api.models.user import User

user = Blueprint('user', __name__)

@user.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400, {'message': 'Missing arguments'})
    if User.query.filter_by(username=username).first() is not None:
        abort(400, {'message': 'Existing user'})
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('user.get_user', id=user.id, _external=True)})


@user.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@user.route('/token')
@auth.login_required
def get_auth_token():
    duration = 600
    token = g.user.generate_auth_token(duration)
    return jsonify({'token': token, 'duration': duration})
