from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'SuperSecretTruedat'
app.config['AUTH_SERVICE_URI'] = "http://127.0.0.1:4000/api/sessions"
app.config['JWT_AUD'] = "trueBG"


from api.v1.group import group
from api.v1.resource import resource
from api.v1.path import path
from api.v1.search import search
from api.v1.session import session


API_V1 = '/api/lineage'

app.register_blueprint(group, url_prefix=API_V1)
app.register_blueprint(resource, url_prefix=API_V1)
app.register_blueprint(path, url_prefix=API_V1)
app.register_blueprint(search, url_prefix=API_V1)
app.register_blueprint(session, url_prefix=API_V1)
