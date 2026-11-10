# REQUISITOS DE INSTALACIÓN

Ejecuta esto comando en la terminal:
```bash
pip install mysql-connector-python
pip install requests
pip install python-dotenv
```
---

# Info

- [Request](https://www.w3schools.com/python/module_requests.asp)
- [Requests Module](https://www.w3schools.com/python/module_requests.asp "Info requests module")
- [MySQL](https://escueladeprogramacion.net/blog/como-conectar-python-con-mysql-guia-paso-a-paso-con-ejemplos)
- [Documentación_API](https://docs.github.com/es/rest?apiVersion=2026-03-10)
- [Cusror_INfo](https://www.geeksforgeeks.org/python/python-sqlite-cursor-object/)


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

```bash
CREATE TABLE IF NOT EXISTS repositorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    html_url VARCHAR(255) NOT NULL,
    watchers_count INT DEFAULT 0,
    stargazers_count INT DEFAULT 0,
    created_at VARCHAR(100),
    updated_at VARCHAR(100)
);
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