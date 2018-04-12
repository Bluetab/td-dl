# -*- coding: utf-8 -*-
from api.app import app
from flask import Blueprint, jsonify
from flask_swagger import swagger


spec = Blueprint('spec', __name__)


@spec.route('/spec', methods=['GET'])
def specSwagger():
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "0.0.1"
    swag['info']['title'] = "Truedat Data Lineage"
    swag['info']['schemas'] = ["http"]
    swag['info']['host'] = "localhost:4003"

    swag['info']['securityDefinitions'] = {
        "bearer":
        {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    }
    swag['info']['security'] = [
        {
            "bearer": []
        }
    ]
    return jsonify(swag)
