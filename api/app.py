from flask import Flask
from flasgger import Swagger
from flask_cors import CORS


template = {
  "swagger": "2.0",
  "info": {
    "title": "Trazabilidad API",
    "description": "API for neo4j traceability model",
    "contact": {
      "responsibleOrganization": "http://bluetab.net/",
      "responsibleDeveloper": "Bluetab",
      "email": "bluetab@bluetab.net",
      "url": "http://bluetab.net/",
    },
    "termsOfService": "http://bluetab.net/",
    "version": "0.0.1"
  },
  "host": "localhost:5000",
  "basePath": "/",
  "schemes": [
    [
      "http",
      "https"
    ]
  ],
  "operationId": "getmyData"
}

app = Flask(__name__)
CORS(app)
Swagger(app, template=template)

from api.v1.group import group
from api.v1.resource import resource
from api.v1.path import path
from api.v1.search import search


API_V1 = '/api/v1'

app.register_blueprint(group, url_prefix=API_V1)
app.register_blueprint(resource, url_prefix=API_V1)
app.register_blueprint(path, url_prefix=API_V1)
app.register_blueprint(search, url_prefix=API_V1)
