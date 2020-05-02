from bottle import abort
from bottle import request
from bottle import static_file
from bottle import template
from bottle import Bottle
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

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

    while True:
        try:
            message = wsock.receive()
            wsock.send("Your message was: %r" % message)
        except WebSocketError:
            break


server = WSGIServer(("0.0.0.0", 8080),
                    app,
                    handler_class=WebSocketHandler)
server.serve_forever()
