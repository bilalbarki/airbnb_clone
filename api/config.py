import os

AIRBNB_ENV = os.environ.get('AIRBNB_ENV')
environments = ["development", "production", "test"]
database_names = {environments[0]: "airbnb_dev", environments[1]: "airbnb_prod", environments[2]:"airbnb_test"}
password_dev = os.environ.get('AIRBNB_DATABASE_PWD_DEV')
password_prod = os.environ.get('AIRBNB_DATABASE_PWD_PROD')
password_test = os.environ.get('AIRBNB_DATABASE_PWD_TEST')

# check for errors in the environment variable AIRBNB_ENV
if AIRBNB_ENV == None:
    print "Please set AIRBNB_ENV environment variable to either %s, %s, or %s!" % (environments[0], environments[1], environments[2])
    quit()
elif AIRBNB_ENV != environments[0] and AIRBNB_ENV != environments[1] and AIRBNB_ENV != environments[2]:
    print "AIRBNB_ENV environment variable has an unsupported value!"
    quit()


if AIRBNB_ENV == environments[0]:
    if password_dev == None:
        print "Please set the environment variable AIRBNB_DATABASE_PWD_DEV with your airnbnb_dev password!"
        quit()
elif AIRBNB_ENV == environments[1]:
    if password_env == None:
        print "Please set the environment variable AIRBNB_DATABASE_PWD_PROD with your airnbnb_prod password!"
        quit()
else:
    if password_env == None:
        print "Please set the environment variable AIRBNB_DATABASE_PWD_TEST with your airnbnb_test password!"
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
        "password": password_dev,
    }

elif AIRBNB_ENV == environments[1]:
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 3000
    DATABASE = {
        "host": "158.69.92.163",
        "user": "airbnb_user_prod",
        "database": database_names[environments[1]],
        "port": 3306,
        "charset": "utf8",
        "password": password_prod,
    }

else:
    DEBUG = False
    HOST = "localhost"
    PORT = 5555
    DATABASE = {
        "host": "158.69.79.7",
        "user": "airbnb_user_test",
        "database": database_names[environments[2]],
        "port": 3306,
        "charset": "utf8",
        "password": password_test,
    }
