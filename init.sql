CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'auth@dbx86';
CREATE USER 'auth_user'@'%' IDENTIFIED BY 'auth@dbx86'; 
CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'%';
USE auth;


CREATE TABLE user (
    id INT NOT NULL PRIMARY KEY auto_increment,
    email VARCHAR(255) NOT NULL UNIQUE ,
    password VARCHAR(255) NOT NULL
);
/*
Adding a test user
*/
INSERT INTO user(email, password) VALUES ('add a valid email for test', 'add a password here');


