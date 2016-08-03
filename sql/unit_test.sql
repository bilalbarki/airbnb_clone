# create users for test
CREATE USER 'airbnb_user_test'@'%' IDENTIFIED BY 'password';

# Create database for test
CREATE DATABASE airbnb_test
       CHARACTER SET utf8
       COLLATE utf8_general_ci;

# grant respective privileges
# airbnb_user_test has all permissions to airbnb_test
GRANT ALL PRIVILEGES ON airbnb_test.* TO 'airbnb_user_test'@'%';
