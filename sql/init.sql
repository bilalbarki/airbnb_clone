# create users for production and development
CREATE USER 'airbnb_user_dev'@'%' IDENTIFIED BY 'password';
CREATE USER 'airbnb_user_prod'@'%' IDENTIFIED BY 'password';

# Create two databases one for production and other for development
CREATE DATABASE airbnb_dev
       CHARACTER SET utf8
       COLLATE utf8_general_ci;

CREATE DATABASE airbnb_prod
       CHARACTER SET utf8
       COLLATE utf8_general_ci;

# grant respective privileges
# airbnb_user_dev has all permissions to airbnb_dev
# airbnb_user_prod has all permissions to airbnb_prod
GRANT ALL PRIVILEGES ON airbnb_dev.* TO 'airbnb_user_dev'@'%';
GRANT ALL PRIVILEGES ON airbnb_prod.* TO 'airbnb_user_prod'@'%';
