from api.app import app
from api.settings.auth import auth
from flask import Blueprint, jsonify
from flask_swagger import swagger


spec = Blueprint('spec', __name__)


@spec.route('/spec', methods=['GET'])
@auth.login_required
def specSwagger():
    swag = swagger(app)
    swag['info']['version'] = "0.0.1"
    swag['info']['title'] = "Truedat Data Lineage"
    return jsonify(swag)
