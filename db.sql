CREATE DATABASE IF NOT EXISTS employee_management;
USE employee_management;
CREATE TABLE IF NOT EXISTS employee_register (
        uid INT NOT NULL AUTO_INCREMENT,
        f_name VARCHAR(40) NOT NULL,
        l_name VARCHAR(40) NOT NULL,
        email VARCHAR(255) NOT NULL,
        contact BIGINT NOT NULL,
        dob DATE NOT NULL,
        join_date DATE NOT NULL,
        gender CHAR(15) NOT NULL,
        PRIMARY KEY (uid)
    );
CREATE TABLE IF NOT EXISTS admin (
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        PRIMARY KEY (username)
    );

CREATE TABLE IF NOT EXISTS employees (
    id INT NOT NULL AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    heure_arrivee TIME NOT NULL,
    heure_sortie TIME NOT NULL,
    poste VARCHAR(100) NOT NULL,
    departement VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);
INSERT INTO admin (username, password) VALUES ('mariam', 'mar123');