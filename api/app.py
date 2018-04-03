from flask import Flask, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('api.settings.config.DevelopmentConfig')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from api.v1.group import group
from api.v1.resource import resource
from api.v1.path import path
from api.v1.search import search
from api.v1.upload import upload
from api.v1.spec import spec


API_V1 = '/api'

app.register_blueprint(group, url_prefix=API_V1)
app.register_blueprint(resource, url_prefix=API_V1)
app.register_blueprint(path, url_prefix=API_V1)
app.register_blueprint(search, url_prefix=API_V1)
app.register_blueprint(upload, url_prefix=API_V1)
app.register_blueprint(spec, url_prefix=API_V1)
