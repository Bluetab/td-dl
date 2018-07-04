from api.common.constants import PORT_DES, PORT_PRO
from api.app import app
import os

class Config(object):
    DEBUG = False
    TESTING = False
    PORT = PORT_DES
    SECRET_KEY = 'SuperSecretTruedat'
    JWT_AUD = 'tdauth'
    ALGORITHM = 'HS512'
    UPLOAD_FOLDER = app.root_path + '/media/uploads'
    ALLOWED_EXTENSIONS = set(['csv', 'zip'])
    NEO4J_HOST = 'localhost'
    NEO4J_PORT = 7687
    NEO4J_USER = 'neo4j'
    NEO4J_PASSWORD = "bluetab"
    EXTERNAL_HOST = 'localhost'
    EXTERNAL_PORT = 4003
    SWAGGER_HOST = "{}:{}".format(EXTERNAL_HOST, EXTERNAL_PORT)


class ProductionConfig(Config):
    APPLICATION_ROOT = '/home/ec2-user/td_dl'
    UPLOAD_FOLDER = os.path.join(APPLICATION_ROOT,
                                 'media/uploads')
    PORT = PORT_PRO
    PATH_NEO4J = '/home/ec2-user/neo4j/lineage'
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT+"/", "")
    EXTERNAL_HOST = 'truedat.bluetab.net'
    EXTERNAL_PORT = 8002
    SWAGGER_HOST = "{}:{}".format(EXTERNAL_HOST, EXTERNAL_PORT)


class NewProductionConfig(Config):
    APPLICATION_ROOT = '/home/ec2-user/td_dl'
    UPLOAD_FOLDER = os.path.join(APPLICATION_ROOT,
                                 'media/uploads')
    PORT = PORT_PRO
    SECRET_KEY = os.getenv('GUARDIAN_SECRET_KEY', 'SuperSecretTruedat')
    PATH_NEO4J = '/home/ec2-user/neo4j/lineage'
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT+"/", "")
    EXTERNAL_HOST = 'truedat.bluetab.net'
    EXTERNAL_PORT = 8002
    NEO4J_HOST = os.getenv('NEO4J_HOST', 'internal-truedatNeo4jELB-420322603.eu-west-1.elb.amazonaws.com')
    NEO4J_PORT = 7687
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'bluetab')
    SWAGGER_HOST = "{}:{}".format(EXTERNAL_HOST, EXTERNAL_PORT)


class DevelopmentConfig(Config):
    APPLICATION_ROOT = os.getcwd()
    DEBUG = True
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT+"/", "")
    PATH_NEO4J = '/home/' + os.environ.get("USER", "ec2-user") + '/neo4j/lineage'


class TestingConfig(Config):
    APPLICATION_ROOT = os.getcwd()
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT+"/", "")
    PATH_NEO4J = '/neo4j'
    TESTING = True
    DEBUG = True
