from datetime import datetime 
from app import app
from app.models.base import db
from flask_json import as_json

app.config['JSON_ADD_STATUS'] = False

@app.route('/', methods=['GET'])
@as_json
def index():
    return dict(
        status="OK", 
        utc_time=datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
        time=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    )

def before_request():
    db.connect()

def after_request():
    db.close()

@app.errorhandler(404)
@as_json
def not_found(error=None):
    return dict(code="404", msg="not found"), 404


'''@app.errorhandler(404)
def page_not_found(error=None):
    return jsonify(code=404, msg="not found"), 404
'''
