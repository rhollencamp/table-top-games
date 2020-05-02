from bottle import abort
from bottle import request
from bottle import static_file
from bottle import template
from bottle import Bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket import Resource
from geventwebsocket import WebSocketError
from geventwebsocket import WebSocketServer
from geventwebsocket.handler import WebSocketHandler

import json
import os
import room


app = Bottle()


@app.get("/")
def index():
    return template("index")


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')


@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    # need to get a message either creating a room or joining a room
    msg = json.loads(wsock.receive())
    if "create" == msg['action']:
        room.create_room(msg, wsock)
    elif "join" == msg['action']:
        room.join_room(msg, wsock)
    else:
        wsock.close()
        return

    while True:
        try:
            message = wsock.receive()
            wsock.send("Your message was: %r" % message)
        except WebSocketError:
            break


server = WSGIServer(("0.0.0.0", int(os.environ['PORT'])),
                    app,
                    handler_class=WebSocketHandler)
server.serve_forever()
