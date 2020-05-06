import json
import os

from bottle import abort
from bottle import request
from bottle import static_file
from bottle import template
from bottle import Bottle
from geventwebsocket import WebSocketError
from geventwebsocket import WebSocketServer

from ttg import room


app = Bottle()


@app.get('/')
def index():
    return template('index')


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
    if msg['msg'] == 'create-game':
        room.create_room(msg, wsock)
    elif msg['msg'] == 'join-game':
        room.join_room(msg, wsock)
    else:
        wsock.close()
        return

    while True:
        try:
            wsock.receive()
        except WebSocketError:
            room.leave_room(wsock)
            break


server = WebSocketServer(('0.0.0.0', int(os.environ['PORT'])),
                         app)
server.serve_forever()
