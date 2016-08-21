bind = "0.0.0.0:3000"
#bind = "%s:%d" % (config.HOST, config.PORT)                                             
workers = 4
errorlog = '/var/log/airbnb_api/gunicorn_error.log'
loglevel = 'info'
accesslog = '/var/log/airbnb_api/gunicorn_access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
