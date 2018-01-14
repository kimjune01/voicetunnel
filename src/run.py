import os

from flask import jsonify, request
from tornado.ioloop import IOLoop
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

import app_file
from sockets.websocket import WebSocket
from src import models
from src.app_file import db

app = app_file.create_app(app_file.config_name)


@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    print("PYTHONPATH: {}".format(os.environ['PYTHONPATH']))
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ])

    print("Running server...")
    if 'PRODUCTION' in os.environ:
        # app.run(host="0.0.0.0", port=int(os.environ['PORT']))
        server.listen(port=int(os.environ['PORT']), address="0.0.0.0")
        IOLoop.instance().start()
    else:
        # app.run()
        server.listen(5000)
        IOLoop.instance().start()