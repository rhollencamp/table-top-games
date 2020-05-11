import os

from geventwebsocket import WebSocketServer

from ttg.webapp import app


server = WebSocketServer(('0.0.0.0', int(os.environ['PORT'])),
                         app)
server.serve_forever()
