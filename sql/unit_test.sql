CREATE DATABASE airbnb_test                                                                      
       DEFAULT CHARACTER SET utf8                                                                  
       DEFAULT COLLATE utf8_general_ci;

/* show databases on server 
\! echo "\nList of databases on servers:"
SHOW DATABASES; */

CREATE USER 'airbnb_user_test'@'localhost' IDENTIFIED BY 'fake_pwd';
CREATE USER 'airbnb_user_test'@'%' IDENTIFIED BY 'fake_pwd';

/* show the users that were created: 
\! echo "\nList of all users:"
SELECT User,Host FROM mysql.user; */

GRANT ALL PRIVILEGES ON airbnb_test.*                                                            
      TO 'airbnb_user_test'@'localhost' IDENTIFIED BY 'fake_pwd';
GRANT ALL PRIVILEGES ON airbnb_test.*
      TO 'airbnb_user_test'@'%' IDENTIFIED BY 'fake_pwd';

FLUSH PRIVILEGES;

/* show updated privileges 
\! echo "\nUpdated privileges"
SELECT * FROM information_schema.user_privileges;*/

