/*
Se puede manejar MARIA-DB desde la consola una vez activada my-sql desde la consola de xammp
c:\xampp\mysql\bin\mysql -u root

Otros comandos útiles para manejarse en elentorno
- SHOW DATABASES;
- USE `base-datos`;
- SHOW TABLES;
- DESCRIBE usuarios;
- SELECT * FROM usuarios;
*/
-----------------------------------------------------------------------------------------------------------------------
-- Creo la base de datos por si no existe:
CREATE DATABASE IF NOT EXISTS `base-datos`;
-----------------------------------------------------------------------------------------------------------------------
-- Creo las tablas usuario:
create TABLE usuarios (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(50) UNIQUE NOT NULL,
    `clave_encrip` VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; --ultima parte buenas practicas evita errores

--Intento de harcodear un usuario, si llego intento CRUD usuario (Usuario: admin | Contraseña: admin123):
INSERT INTO `usuarios` (`id`, `nombre`, `clave_encrip`) VALUES
(1, 'admin', 'admin123');

---------------------
-- Tablas APIs

CREATE TABLE IF NOT EXISTS repositorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner VARCHAR(100) NOT NULL,
    name VARCHAR(150) NOT NULL,
    html_url VARCHAR(255) NOT NULL,
    stargazers_count INT DEFAULT 0,
    created_at VARCHAR(100),
    updated_at VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS followers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seleccionado VARCHAR(100) NOT NULL,
    f_name VARCHAR(150) NOT NULL,
    f_html_url VARCHAR(255) NOT NULL,
    f_type VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

