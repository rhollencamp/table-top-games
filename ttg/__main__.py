import os

from ttg.webapp import app


app.run(host="0.0.0.0",
        port=int(os.environ['PORT']),
        access_log=False,
        debug=False)
