import os

AIRBNB_ENV = os.environ.get('AIRBNB_ENV')

# check for errors in the environment variable AIRBNB_ENV
if AIRBNB_ENV == None:
    print "Please set AIRBNB_ENV environment variable to either production or development!"
    quit()
elif AIRBNB_ENV != "development" or AIRBNB_ENV != "production":
    print "AIRBNB_ENV environment variable has an unsupported value!"
    quit()

# set appropriate variables depending on development or production
if AIRBNB_ENV == "development":
    DEBUG = True
    HOST = "localhost"
    PORT = "3333"
    DATABASE = {
        "host": "158.69.92.163", 
        "user": "airbnb_user_dev",
        "port": "3306",
        "charset": "utf8",
        "password": os.environ.get('AIRBNB_DATABASE_PWD_DEV'),
    }

else:
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = "3000"
    DATABASE = {
        "host": "158.69.92.163",
        "user": "airbnb_user_prod",
        "port": "3306",
        "charset": "utf8",
        "password": os.environ.get('AIRBNB_DATABASE_PWD_PROD'),
    }
