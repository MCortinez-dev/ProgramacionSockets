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

## 🚀 Cómo Ejecutar el Proyecto

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
