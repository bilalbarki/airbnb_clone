from app import app
import config
from flask_cors import CORS, cross_origin

if __name__ == "__main__":
	app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
	app.config['JSON_ADD_STATUS'] = False

