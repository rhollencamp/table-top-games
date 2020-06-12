from os import getenv

from sanic.websocket import WebSocketProtocol

from ttg.webapp import app


app.run(host="0.0.0.0",
        port=int(getenv('PORT', '8080')),
        protocol=WebSocketProtocol,
        access_log=False,
        debug=False)
