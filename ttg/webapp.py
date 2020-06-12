from sanic import Sanic

from ttg.net import new_connection_established


def _create_sanic_web_config():
    """
    Sanic log configuration to avoid duplicate messages

    Default log configuration Sanic uses has handlers set up that causes
    messages to be logged twice, so pass in a minimal config of our own to
    avoid those handlers being created / used
    """

    return dict(
        version=1,
        disable_existing_loggers=False,
        loggers={
            "sanic.root": {"level": "INFO"},
            "sanic.error": {"level": "INFO"},
            "sanic.access": {"level": "INFO"},
        }
    )


async def _websocket(_, wsock):
    """handler for new websocket connections"""
    await new_connection_established(wsock)


app = Sanic(__name__, log_config=_create_sanic_web_config())

# home / index static route
app.static('/', './static/index.html')
# static assets route
app.static('/static', './static')
# websocket route
app.add_websocket_route(_websocket, '/websocket')
