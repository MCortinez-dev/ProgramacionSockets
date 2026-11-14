Markdown

# ✨ Programación Sobre Redes

El presente Proyecto desarrollado la teoría y práctica para la Programación sobre Redes utilizando Sockets TCP (`AF_INET`, `SOCK_STREAM`) y concurrencia con hilos (`threading`) en Python. El mismo contine tres carpetas pricipales:
- cliente-servidor-1er-ejercicio <-- Primer ejecicio centrado en la comprensión de threading
- teoria_theading_sockets <-- Bases teórica de las clases
- tp-final <-- Trabajo práctico final presentado en la matería

Mas abajo se detalla una explicación general y el funcionamiento del 1er ejercicio y del TP Final.

---
## 📂 Estructura del Proyecto
```
/
|   .env
|   .gitignore
|   README.md
|   
+---cliente-servidor-1er-ejercicio
|       (cliente.py) + (clienteXboot.py) ---------# Cliente manejado, mas simulados
|       Info.md ----------------------------------# Información leida o recopilada durante el desarrollo
|       lanzador_automatico_linux.sh -------------# Lanzador automatico para probar en linux abre varias ventanas
|       lanzador_automatico_windows.bat ----------# Lanzador automatico para probar en linux abre varias ventanas
|       servidor.py # Servidor
|       
+---teoria_theading_sockets ----------------------# Archivos e imagenes de apoyo teórico práctico
|           
+---tp-final
        base-datos.sql ---------------------------# Comandos para crear tablas necesarias e información interesante
        cliente.py
        consigna.md ------------------------------# Consigna a cumplir por el TP
        requirements.txt -------------------------# Para pip install
        servidor.py
        Notas.md ---------------------------------# Información leida o recopilada durante el desarrollo
        

``` 
---

## 🚀 Cómo Ejecutar ▶️ cliente-servidor-1er-ejercicio

### 🌟 Opción Automática (Recomendada)
Para simular el entorno completo con el servidor, el cliente interactivo y múltiples bots corriendo en paralelo con un solo clic:
* **En Windows:** Ejecuta el archivo `lanzar_todo.bat`
* **En Linux:** Ejecuta el script `./lanzar_todo.sh`

### 🛠️ Opción Manual
1. Inicia el servidor en una terminal:
   ```bash
   python servidor.py
   ```

2. Abre terminales adicionales y ejecuta el cliente interactivo o los bots:
   ````bash
    python cliente.py
   ````

### ⌨️ Comandos Disponibles para el Cliente

* Texto libre: Envía mensajes al servidor que responderá con un eco formateado con colores ANSI.
* /users: Consulta al servidor la cantidad y estado de los usuarios conectados en tiempo real.
* /adios: Cierra la sesión de manera ordenada, eliminando el socket de la lista de conexiones activas.

---

## 🚀 Cómo Ejecutar ▶️ tp-final

El Trabajo Práctico Final integra un servidor TCP concurrente basado en hilos (`threading`), base de datos con MariaDB/MySQL y consumo de la API REST de GitHub con autenticación por token.

### ⚙️ Prerrequisitos y Configuración Inicial

1. **Base de Datos:** 
   - Asegúrate de tener activo MariaDB (por ejemplo, desde el panel de control de XAMPP).
   - Importa el archivo `base-datos.sql` provisto en la carpeta para crear automáticamente la estructura de la base de datos y las tablas necesarias (`usuarios`, `repositorios`, `followers`).

2. **Dependencias:**
   - Instala las librerías externas requeridas ejecutando en tu terminal:
     ```bash
     pip install -r requirements.txt
     ```

3. **Variables de Entorno (`.env`):**
- Crea un archivo llamado `.env` en la raíz del proyecto configurando las credenciales de acceso a tu base de datos y tu token personal de GitHub (indispensable para evitar el bloqueo por límite de peticiones de la API - Error 403):
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=base-datos
GITHUB_TOKEN=tu_token_personal_de_github
```

### 🕹️ Instrucciones de Ejecución

1. **Iniciar el Servidor:**
Abre una terminal, posicionate en la carpeta `tp-final` y ejecuta:
```bash
python servidor.py
```

2. **Iniciar el Cliente:**
Abre otra terminal (puedes abrir múltiples instancias para probar la concurrencia entre varios clientes), posicionate en la carpeta `tp-final` y ejecuta:
```bash
python cliente.py
```

* El sistema te solicitará por consola tus credenciales de acceso (puedes utilizar el usuario administrador por defecto: **Usuario:** `admin` | **Contraseña:** `admin123`).

### ⌨️ Comandos Disponibles en el Chat del TP Final

Una vez autenticado con éxito en el servidor, puedes utilizar los siguientes comandos escribiendolos en la consola:

* `/usuarios`: Consulta en tiempo real la cantidad de clientes activos conectados al servidor.
* `/hora`: Solicita y muestra la hora actual del servidor.
* `/todos [mensaje]` : Envía un mensaje a todos los usuarios conectados desde el lado del cliente.
* `/repos [usuario_github]`: Consulta los repositorios públicos de un usuario a través de la API de GitHub, los muestra formateados en pantalla y los almacena de forma persistente en la tabla `repositorios` de la base de datos.
* `/followers [usuario_github]`: Consulta los seguidores de un usuario en la API de GitHub y los guarda de forma persistente en la tabla `followers`.
* `/adios`: Finaliza la sesión de manera ordenada, cerrando el socket, notificando al servidor y liberando los recursos activos.
* *Texto libre:* Envía un mensaje general de chat con marcas de tiempo y formato de colores ANSI.
