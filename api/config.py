import os

##############################################################
# ===> SECTION: DATABASE INFO

environments = [
	   "development",
	   "production", 
	   "test",
	]

database_names = {
	   environments[0]: "airbnb_dev", 
	   environments[1]: "airbnb_prod", 
	   environments[2]: "airbnb_test",
	}

############################################################
# ===> SECTION: GET VALUES FROM ENV VARIABLES
# @AIRBNB_ENV -> development/production/test
# @PASSWORD_X -> password to access the specific database
AIRBNB_ENV = os.environ.get('AIRBNB_ENV')
PASSWORD_DEV = os.environ.get('AIRBNB_DATABASE_PWD_DEV')
PASSWORD_PROD = os.environ.get('AIRBNB_DATABASE_PWD_PROD')
PASSWORD_TEST = os.environ.get('AIRBNB_DATABASE_PWD_TEST')

##############################################################
# ===> SECTION: ERROR TESTING
# check for errors in the environment variable AIRBNB_ENV

if AIRBNB_ENV == None:
    print "Please set AIRBNB_ENV environment variable to either %s, %s or %s!" % (environments[0], environments[1], environments[2])
    quit()
elif AIRBNB_ENV != environments[0] and AIRBNB_ENV != environments[1] and AIRBNB_ENV != environments[2]:
    print "AIRBNB_ENV environment variable has an unsupported value!"
    quit()

# check if password was set properly in the respective envionment variable
if AIRBNB_ENV == environments[0]:
    if PASSWORD_DEV == None:
        print "Please set the environment variable AIRBNB_DATABASE_PWD_DEV with your airnbnb_dev password!"
        quit()

elif AIRBNB_ENV == environments[1]:
    if PASSWORD_PROD == None:
        print "Please set the environment variable AIRBNB_DATABASE_PWD_PROD with your airnbnb_prod password!"
        quit()
else:
    if PASSWORD_TEST == None:
        print "Please set the environment variable AIRBNB_DATABASE_PWD_TEST with your airnbnb_test password!"
        quit()


##############################################################
# ===> SECTION: SET APPROPRIATE CONFIG VARIABLES
# set appropriate variables depending on development or production

if AIRBNB_ENV == environments[0]: # airbnb_dev
    DEBUG = True
    HOST = "localhost"
    PORT = 3333
    ALLOW_CORS = "*"
    DATABASE = {
        "host": "158.69.92.163", 
        "user": "airbnb_user_dev",
        "database": database_names[environments[0]],
        "port": 3306,
        "charset": "utf8",
        "password": PASSWORD_DEV,
    }

elif AIRBNB_ENV == environments[1]: # airbnb_prod
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 3000
    ALLOW_CORS = ["158.69.92.163","52.91.150.68"]
    DATABASE = {
        "host": "158.69.92.163",
        "user": "airbnb_user_prod",
        "database": database_names[environments[1]],
        "port": 3306,
        "charset": "utf8",
        "password": PASSWORD_PROD,
    }

else: # airbnb_test
    DEBUG = False
    HOST = "localhost"
    PORT = 5555
    ALLOW_CORS = "*"
    DATABASE = {
        "host": "158.69.92.163",
        "user": "airbnb_user_test",
        "database": database_names[environments[2]],
        "port": 3306,
        "charset": "utf8",
        "password": PASSWORD_TEST,
    }
