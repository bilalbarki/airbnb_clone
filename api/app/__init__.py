from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS, cross_origin
import config

import logging
from logging.handlers import RotatingFileHandler

class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno == self.__level

app = Flask(__name__)
json = FlaskJSON(app)
app.config['JSON_ADD_STATUS'] = False
cors = CORS(app, resources={r"/*": {"origins": config.ALLOW_CORS}})

# logging for warnings
warning_handler = RotatingFileHandler('./logs/warnings.log', maxBytes=10*1024*1024, backupCount=1)
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(MyFilter(logging.WARNING))
app.logger.addHandler(warning_handler)

# logging for errors and critical
error_handler = RotatingFileHandler('./logs/errors.log', maxBytes=10*1024*1024, backupCount=1)
error_handler.setLevel(logging.ERROR)
app.logger.addHandler(error_handler)

#logging for web requests
access_handler = RotatingFileHandler('./logs/access.log', maxBytes=10*1024*1024, backupCount=1)
access_logger = logging.getLogger('werkzeug')
access_logger.addHandler(access_handler)

# logging for database queries
peewee_handler = RotatingFileHandler('./logs/database.log', maxBytes=10*1024*1024, backupCount=1)
peewee_logger = logging.getLogger('peewee')
peewee_logger.setLevel(logging.DEBUG)
peewee_logger.addHandler(peewee_handler)

from app.views import *
