import sys
import urllib
import threading

sys.path.append("..")

from webapp import app
from flask import request
from db import Database

app.config['DATABASE']  = 'test_data.db'
app.config['UPDATE_INTERVAL'] = 1000
app.config['ENABLE_LONG_POLL'] = False

UPDATE_INTERVAL = app.config['UPDATE_INTERVAL'] / 1000.0

HOST = 'localhost'
PORT = 5001
SERVER_URL = 'http://%s:%s/' % (HOST, PORT)

from logging import StreamHandler
app.logger.addHandler(StreamHandler())

server = threading.Thread(target=lambda: app.run(host=HOST, port=PORT, debug=False))

def start_test_server():
    Database(app.config["DATABASE"]).init()
    server.start()

def shutdown_test_server():
    urllib.urlopen(SERVER_URL + 'shutdown')
    server.join()

@app.route("/shutdown")
def shutdown_server_handler():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return ""