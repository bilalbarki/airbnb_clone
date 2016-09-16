from datetime import datetime 
from app import app
from app.models.base import db
from flask_json import as_json

'''for testing api status'''
@app.route('/', methods=['GET'])
@as_json
def index():
	return dict(
		status="OK", 
		utc_time=datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"),
		time=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

'''an error handler for unknown requests'''
@app.errorhandler(404)
@as_json
def not_found(error=None):
    return dict(code=404, msg="not found"), 404
