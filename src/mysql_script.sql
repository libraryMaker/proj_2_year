show databases;
root 746td215
create database product;
CREATE USER 'user_cli'@'localhost' IDENTIFIED BY 'pass';
GRANT SELECT ON product.* TO 'user_cli'@'localhost';
GRANT INSERT ON product.* TO 'user_cli'@'localhost';
FLUSH PRIVILEGES;
CREATE TABLE product.sensors_data (
    id bigint NOT NULL AUTO_INCREMENT,
    temperature decimal(5, 2),
    humidity decimal(3, 0),
    co2 decimal(4, 0),
    insertion_date datetime,
    PRIMARY KEY (id)
);

CREATE INDEX id_index ON product.sensors_data (id, insertion_date);
delimiter $$
CREATE TRIGGER product.ins_time BEFORE INSERT ON sensors_data
       FOR EACH ROW
           SET NEW.insertion_date = SYSDATE();
$$delimiter;
