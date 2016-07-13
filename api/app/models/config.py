import os

AIRBNB_ENV = os.environ.get('AIRBNB_ENV')
environments = ["development", "production"]
database_names = {environments[0]: "airbnb_dev", environments[1]: "airbnb_prod"}

# check for errors in the environment variable AIRBNB_ENV
if AIRBNB_ENV == None:
    print "Please set AIRBNB_ENV environment variable to either %s or %s!" % (environments[0], environments[1])
    quit()
elif AIRBNB_ENV != environments[0] and AIRBNB_ENV != environments[1]:
    print "AIRBNB_ENV environment variable has an unsupported value!"
    quit()

# set appropriate variables depending on development or production
if AIRBNB_ENV == environments[0]:
    DEBUG = True
    HOST = "localhost"
    PORT = 3333
    DATABASE = {
        "host": "158.69.92.163", 
        "user": "airbnb_user_dev",
        "database": database_names[environments[0]],
        "port": 3306,
        "charset": "utf8",
        "password": os.environ.get('AIRBNB_DATABASE_PWD_DEV'),
    }

else:
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 3000
    DATABASE = {
        "host": "158.69.92.163",
        "user": "airbnb_user_prod",
        "database": database_names[environments[1]],
        "port": 3306,
        "charset": "utf8",
        "password": os.environ.get('AIRBNB_DATABASE_PWD_PROD'),
    }
