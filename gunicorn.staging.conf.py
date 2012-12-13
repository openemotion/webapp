workers = 4
worker_class = "gevent"
bind = "unix:/home/staging/webapp/var/gunicorn.sock"
accesslog = "/home/staging/webapp/var/access.log"
errorlog = "/home/staging/webapp/var/error.log"
