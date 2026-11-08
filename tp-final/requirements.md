# REQUISITOS DE INSTALACIÓN

Ejecuta esto comando en la terminal:
```bash
pip install mysql-connector-python
pip install requests
pip install python-dotenv
```
---

# Info

[MySQL](https://escueladeprogramacion.net/blog/como-conectar-python-con-mysql-guia-paso-a-paso-con-ejemplos)


# Base de datos
Comando terminal(evita el explorador)
```bash
c:\xampp\mysql\bin\mysql -u root
```

Otros comandos:
```Bash
USE `base-datos`;

CREATE TABLE IF NOT EXISTS usuarios (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(50) UNIQUE NOT NULL,
    `clave_encrip` VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
```

```Bash
INSERT INTO `usuarios` (`id`, `nombre`, `clave_encrip`) VALUES
(1, 'admin', '$2y$10$IwjNFFVUk8SnHO.jORhN0OyhO15nJM7947BbOyxM6GSa5C/sKN1FK');
```

```Bash
SHOW DATABASES;
````
```Bash
USE `base-datos`;
````
```Bash
SHOW TABLES;
````
```Bash
DESCRIBE usuarios;
````
```Bash
SELECT * FROM usuarios;
```