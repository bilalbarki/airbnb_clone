description "Gunicorn application server running airbnb_clone api"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid admin
setgid www-data

env AIRBNB_ENV=production
env AIRBNB_DATABASE_PWD_PROD=passwordhere
chdir /var/airbnb_clone/api

# gunicorn_config.py defines the configuration for gunicorn                   
exec gunicorn -c gunicorn_config.py wsgi

