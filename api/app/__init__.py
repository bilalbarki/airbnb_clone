from flask import Flask
from flask_json import FlaskJSON
#from app.views import *
from flask_cors import CORS, cross_origin
import config

app = Flask(__name__)
json = FlaskJSON(app)
app.config['JSON_ADD_STATUS'] = False
cors = CORS(app, resources={r"/*": {"origins": config.ALLOW_CORS}})

from app.views import *
