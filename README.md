Markdown

# ✨ Sistema de Sockets TCP Multi-hilo en Python

Proyecto desarrollado para Programación sobre Redes utilizando Sockets TCP (`AF_INET`, `SOCK_STREAM`) y concurrencia con hilos (`threading`) en Python.

---

## 📂 Estructura del Proyecto

* **`servidor.py`**: Servidor central multihilo que gestiona conexiones simultáneas, el control de la lista de clientes activos y el procesamiento de comandos.
* **`cliente.py`**: Cliente interactivo por teclado con estilos ANSI personalizados y soporte para comandos especiales.
* **`cliente1boot.py` al `cliente9boot.py`**: Scripts de bots automatizados para pruebas de estrés y concurrencia en paralelo.
* **Lanzadores Automáticos**: Scripts diseñados para levantar todos los procesos de forma independiente en Windows (`.bat`) y Linux (`.sh`).
  
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

## ⌨️ Comandos Disponibles para el Cliente

* Texto libre: Envía mensajes al servidor que responderá con un eco formateado con colores ANSI.
* /users: Consulta al servidor la cantidad y estado de los usuarios conectados en tiempo real.
* /adios: Cierra la sesión de manera ordenada, eliminando el socket de la lista de conexiones activas.
