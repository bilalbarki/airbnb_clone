from app import app
import config
from flask_cors import CORS, cross_origin

'''NOTE: you might need the option threaded=True in app.run'''
if __name__ == "__main__":
	app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
