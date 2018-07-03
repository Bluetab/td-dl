from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from healthcheck import HealthCheck

import os


environ = os.getenv("APP_ENV", "Development") if \
    os.getenv("APP_ENV", "Development") in ["Development", "Production", "Testing", "NewProduction"] \
    else "Development"

app = Flask(__name__)

health = HealthCheck(app, "/health")

CORS(app)
app.config.from_object('api.settings.config.{}Config'.format(environ))

app.config['SWAGGER'] = {
    'title': 'Truedat Data Lineage API',
    'uiversion': 3
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Truedat Data Lineage API",
        "description": "Truedat Data Lineage API",
        "version": "0.0.1"
    },
    "host": app.config['SWAGGER_HOST'],
    "schemes": ["http"],
    "securityDefinitions": {
        "bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "security": [{ "bearer": []}]
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/api/swagger"
}

Swagger(app, template=swagger_template, config=swagger_config)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from api.v1.group import group
from api.v1.resource import resource
from api.v1.path import path
from api.v1.search import search
from api.v1.metadata import metadata
from api.v1.writeNeo4j import writeNeo4j

API_V1 = '/api'

app.register_blueprint(group, url_prefix=API_V1)
app.register_blueprint(resource, url_prefix=API_V1)
app.register_blueprint(path, url_prefix=API_V1)
app.register_blueprint(search, url_prefix=API_V1)
app.register_blueprint(metadata, url_prefix=API_V1)
app.register_blueprint(writeNeo4j, url_prefix=API_V1)
