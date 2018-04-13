from multiprocessing import Process
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado import ioloop
from api.app import app

def run_server():
    DEFAULT_APP_TCP_PORT = app.config['PORT']

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(DEFAULT_APP_TCP_PORT)

    ioloop.IOLoop.instance().start()


def before_all(context):
    context.server_thread = Process(target=run_server)
    context.server_thread.deamon = True
    context.server_thread.start()

def after_all(context):
    context.server_thread.terminate()