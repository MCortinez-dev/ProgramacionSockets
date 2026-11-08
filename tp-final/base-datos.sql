-- Creo la base de datos por si no existe:
CREATE DATABASE IF NOT EXISTS `base-datos`;
USE `base-datos`;

-----------------------------------------------------------------------------------------------------------------------
-- Creo las tablas usuario:
create TABLE usuarios (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(50) UNIQUE NOT NULL,
    `clave_encrip` VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci; //ultima parte buenas practicas evita errores

--Intento de harcodear un usuario, si llego intento CRUD usuario (Usuario: admin | Contraseña: admin123):
INSERT INTO `usuarios` (`id`, `nombre`, `clave_encrip`) VALUES
(1, 'admin', 'admin123');

---------------------
-- Tablas APIs