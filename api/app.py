from app import app
import config

'''NOTE: you might need the option threaded=True in app.run'''
if __name__ == "__main__":
	app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
