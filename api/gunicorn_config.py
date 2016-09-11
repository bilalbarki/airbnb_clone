import os, sys
base = os.path.dirname(os.path.dirname(__file__))                                                                                             
sys.path.append(base)

from config import HOST, PORT
bind = "%s:%d" % (HOST, PORT)
workers = 4
errorlog = '/var/log/airbnb_api/gunicorn_error.log'
loglevel = 'info'
accesslog = '/var/log/airbnb_api/gunicorn_access.log'
reload = True
