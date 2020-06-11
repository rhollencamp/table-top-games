from sanic import Sanic

from ttg.net import new_connection_established


__sanic_log_config = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO"},
        "sanic.error": {"level": "INFO"},
        "sanic.access": {"level": "INFO"},
    }
)

app = Sanic(__name__, log_config=__sanic_log_config)

# home / index
app.static('/', './static/index.html')

# static directory
app.static('/static', './static')


@app.websocket('/websocket')
async def feed(_, wsock):
    await new_connection_established(wsock)
