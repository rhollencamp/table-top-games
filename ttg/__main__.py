import os

from sanic.websocket import WebSocketProtocol

from ttg.webapp import app


app.run(host="0.0.0.0",
        port=int(os.environ['PORT']),
        protocol=WebSocketProtocol,
        access_log=False,
        debug=False)
