CREATE DATABASE IF NOT EXISTS habi;
USE habi;

CREATE TABLE IF NOT EXISTS properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state ENUM('pre_venta', 'en_venta', 'vendido') NOT NULL,
    construction_year INT NOT NULL,
    price DECIMAL(15, 2) NOT NULL, -- Se cambió DECIMAL(10, 2) a DECIMAL(15, 2)
    description TEXT
);

-- Insertando datos iniciales
INSERT INTO properties (address, city, state, construction_year, price, description)
VALUES
    ('Calle Falsa 123', 'Bogota', 'pre_venta', 2023, 150000000.00, 'Hermoso apartamento nuevo en una zona exclusiva.'),
    ('Avenida Siempre Viva 456', 'Medellin', 'en_venta', 2020, 120000000.00, 'Amplia casa en el centro de la ciudad.'),
    ('Calle 98 #12-34', 'Cali', 'vendido', 2019, 90000000.00, 'Apartamento de 3 habitaciones, muy cerca al centro.'),
    ('Carrera 7 #45-67', 'Barranquilla', 'en_venta', 2021, 200000000.00, 'Apartamento moderno, con acabados de lujo.'),
    ('Calle 50 #24-56', 'Cartagena', 'pre_venta', 2024, 180000000.00, 'Proyecto de apartamentos con vista al mar.');