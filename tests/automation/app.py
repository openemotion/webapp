import os
import sys
import urllib
import threading

APPROOT = os.path.realpath((os.path.split(__file__)[0] or '.') + '/../..')
print APPROOT
sys.path.append(APPROOT)

from flask import request

os.environ['OPENEM_CONFIG'] = 'config.selenium'
from webapp import app, db

HOST = 'localhost'
PORT = 5001
SERVER_URL = 'http://%s:%s/' % (HOST, PORT)

from logging import StreamHandler
app.logger.addHandler(StreamHandler())

server = threading.Thread(target=lambda: app.run(host=HOST, port=PORT, debug=False))

def start_test_server():
    with app.app_context():
        db.drop_all()
        db.create_all()
    server.start()

def shutdown_test_server():
    urllib.urlopen(SERVER_URL + 'shutdown')
    server.join()

@app.route('/shutdown')
def shutdown_server_handler():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return ''