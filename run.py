#!venv/bin/python
# Run with tornado
from tornado import autoreload
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from api.app import app


DEFAULT_APP_TCP_PORT = 4003

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(DEFAULT_APP_TCP_PORT)
ioloop = IOLoop.instance()
autoreload.start(ioloop)
ioloop.start()
