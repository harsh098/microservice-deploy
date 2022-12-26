CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'auth@dbx86';
CREATE DATABASE auth;
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
USE auth;


CREATE TABLE user (
    id INT NOT NULL PRIMARY KEY auto_increment,
    email VARCHAR(255) NOT NULL UNIQUE ,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user(email, password) VALUES ('admin', 'root@admin');


