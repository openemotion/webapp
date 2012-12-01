workers = 4
worker_class = "gevent"
bind = "unix:/home/openemotion/webapp/var/gunicorn.sock"
accesslog = "/home/openemotion/webapp/var/access.log"
errorlog = "/home/openemotion/webapp/var/error.log"
