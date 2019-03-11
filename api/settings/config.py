from api.app import app
import os


class Config(object):
    # Application settings
    APPLICATION_ROOT = os.getenv('APPLICATION_ROOT')
    DEBUG = os.getenv('DEBUG') == 'true'
    TESTING = os.getenv('TESTING') == 'true'
    PORT = int(os.getenv('API_PORT', default='4003'))
    # Authentication
    ALGORITHM = 'HS512'
    JWT_AUD = 'tdauth'
    SECRET_KEY = os.getenv('GUARDIAN_SECRET_KEY')
    # File uploads
    ALLOWED_EXTENSIONS = set(['csv', 'zip'])
    METADATA_SCRIPT = os.getenv('METADATA_SCRIPT')
    UPLOAD_PATH = os.getenv(
        'UPLOAD_PATH',
        default=os.path.join(
            APPLICATION_ROOT,
            'media/uploads'))
    # Swagger config
    EXTERNAL_HOST = os.getenv('EXTERNAL_HOST', default=os.getenv('HOSTNAME'))
    EXTERNAL_PORT = int(os.getenv('EXTERNAL_PORT', default='4003'))
    SWAGGER_HOST = '{}:{}'.format(EXTERNAL_HOST, EXTERNAL_PORT)
    SWAGGER_ROOT = app.root_path.replace(APPLICATION_ROOT + '/', '')
    # Neo4j config
    NEO4J_HOST = os.getenv('NEO4J_HOST', default='neo4j')
    NEO4J_PORT = int(os.getenv('NEO4J_PORT', default='7687'))
    NEO4J_USER = os.getenv('NEO4J_USER', default='neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', default='neo4j')
    # Redis config
    REDIS_HOST = os.getenv('REDIS_HOST', default='redis')
    REDIS_URI = 'redis://' + REDIS_HOST
