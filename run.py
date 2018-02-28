#!venv/bin/python
# Run with tornado
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from api.app import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(4002)
IOLoop.instance().start()
