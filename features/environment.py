from behave import fixture, use_fixture
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from multiprocessing import Process
from tornado.ioloop import IOLoop
from tornado import autoreload
from api.app import app

@fixture
def flaskr_client(context, *args, **kwargs):

    DEFAULT_APP_TCP_PORT = app.config['PORT']
    #
    # http_server = HTTPServer(WSGIContainer(app))
    # http_server.listen(DEFAULT_APP_TCP_PORT)
    # ioloop = IOLoop.instance()
    #
    #
    # p = Process(target=autoreload.start(ioloop), args=())
    # p.daemon = True                       # Daemonize it
    # p.start()

def before_feature(context, feature):
    # -- HINT: Recreate a new flaskr client before each feature is executed.
    use_fixture(flaskr_client, context)
