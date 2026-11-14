# Apuntes y Referencias: Módulo de Sockets en Python

## 1. Creación y Configuración del Socket

```python
class socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)

```

* **Descripción:** Crea un nuevo socket utilizando la familia de direcciones, el tipo de socket y el número de protocolo especificados.
* **Parámetros:**
* `family`: `AF_INET` (por defecto para IPv4), `AF_INET6`, `AF_UNIX`, `AF_CAN`, `AF_PACKET`, o `AF_RDS`.
* `type`: `SOCK_STREAM` (por defecto para TCP), `SOCK_DGRAM`, `SOCK_RAW`, entre otras constantes `SOCK_`.
* `proto`: Número de protocolo (por defecto `0`, se puede omitir).
* `fileno`: Si se especifica, los valores de `family`, `type` y `proto` se detectan automáticamente a partir del descriptor de archivo indicado.


* **Propiedad:** El socket recién creado es **no heredable** (*non-inheritable*).

---

## 2. Conexión Avanzada de Clientes

```python
socket.create_connection(address, timeout=GLOBAL_DEFAULT, source_address=None, *, all_errors=False)

```

* **Descripción:** Conecta a un servicio TCP que escucha en una dirección de Internet (tupla de 2 elementos `(host, port)`) y retorna el objeto socket.
* **Ventajas frente a `socket.connect()`:** Es una función de nivel superior. Si el `host` es un nombre de host no numérico, intentará resolverlo tanto para `AF_INET` como para `AF_INET6`, probando todas las direcciones posibles de manera secuencial hasta que una conexión prospere (ideal para compatibilidad dual).
* **Parámetros opcionales:**
* `timeout`: Configura el tiempo de espera en el socket antes de intentar la conexión.
* `source_address`: Tupla `(host, port)` para enlazar la dirección de origen antes de conectar.
* `all_errors`: Si está en `True`, ante un fallo general retorna un `ExceptionGroup` con los errores de todos los intentos.



---

## 3. Opciones de Configuración Avanzada (`setsockopt`)

```python
setsockopt(level, optname, value: int | Buffer)
setsockopt(level, optname, None, optlen: int)

```

* **Descripción:** Permite configurar opciones a bajo nivel en el socket (equivalente a la función `setsockopt` de la API de C en sistemas Unix).

### Opciones principales y su utilidad práctica en servidores:

* **`0. socket.SOL_SOCKET` (El Nivel):**
* Indica al sistema operativo que la configuración pertenece a la capa general de sockets y no a un protocolo específico como TCP (`IPPROTO_TCP`).


* **1. `SO_REUSEADDR` (Nivel: `socket.SOL_SOCKET`):**
* Permite reutilizar la dirección IP y el puerto de forma inmediata.
* **Uso:** Evita el error clásico de *"Address already in use"* (Dirección ya en uso) cuando cerrás un servidor y querés volver a levantarlo rápidamente.


* **2. `SO_KEEPALIVE` (Nivel: `socket.SOL_SOCKET`):**
* Activa señales automáticas de "latido" (*heartbeat*) en segundo plano.
* **Uso:** Detecta si un cliente pierde la conexión de forma abrupta (se apaga el dispositivo o se corta el Wi-Fi) sin enviar un cierre formal, liberando memoria en el servidor.


* **3. `TCP_NODELAY` (Nivel: `socket.IPPROTO_TCP`):**
* Desactiva el *Algoritmo de Nagle* (sistema que agrupa pequeños paquetes para ahorrar ancho de banda).
* **Uso:** Fundamental para aplicaciones en tiempo real (chats interactivos, juegos online) donde cada `send()` debe enviarse de inmediato sin demoras.


* **4. `SO_RCVBUF` y `SO_SNDBUF` (Nivel: `socket.SOL_SOCKET`):**
* Modifican el tamaño (en bytes) de los búferes de recepción y envío del sistema operativo.
* **Uso:** Optimización avanzada para transferencia masiva de datos (archivos pesados o streaming).


* **5. `SO_BROADCAST` (Nivel: `socket.SOL_SOCKET`):**
* Autoriza a un socket (habitualmente UDP) a enviar mensajes de difusión a toda la red local.
* **Uso:** Aplicaciones de descubrimiento automático de servidores en una misma red Wi-Fi.



---

## 4. Análisis de Excepción: Error al salir (`/adios`)

### Traza del Error (Log del Sistema)

```text
[('127.0.0.1', 28441)] dice: /adios
Exception in thread Thread-1 (manejar_cliente):
Traceback (most recent call last):
  File "C:\Users\fudom\AppData\Local\Python\pythoncore-3.14-64\Lib\threading.py", line 1082, in _bootstrap_inner
    self._context.run(self.run)
  File "C:\Users\fudom\AppData\Local\Python\pythoncore-3.14-64\Lib\threading.py", line 1024, in run
    self._target(*self._args, **self._kwargs)
  File "d:\Git-Hub\Sockets\cliente-servidor-cortinez\servidor.py", line 14, in manejar_cliente
    mensaje = conn.recv(1024).decode('utf-8') 
ConnectionAbortedError: [WinError 10053] Se ha anulado una conexión establecida por el software en su equipo host

```

### Diagnóstico del Problema:

* **Excepción:** `ConnectionAbortedError: [WinError 10053]`
* **Causa:** Ocurre en el hilo del servidor cuando el cliente corta la conexión de manera abrupta (o envía el comando `/adios` y cierra el socket del lado cliente sin dar tiempo a que el servidor complete el ciclo de lectura pendiente en `conn.recv()`). El sistema operativo Windows aborta la tubería de comunicación activa de forma imprevista.
* **Solución recomendada:** Envolver siempre las operaciones de lectura/escritura del servidor (`conn.recv()` / `conn.send()`) dentro de bloques estructurados de manejo de excepciones (`try-except`) para interceptar la desconexión limpia sin que colapse el hilo del cliente.

---

## 5. Bibliografía y Enlaces de Interés

* **Documentación Oficial Python:**
* [Módulo Socket](https://docs.python.org/3/library/socket.html)
* [Módulo SocketServer](https://docs.python.org/3/library/socketserver.html#module-socketserver)
* [Módulo Threading](https://docs.python.org/3/library/threading.html)


* **Guías y Recursos Externos:**
* [Uso de F-Strings en Python (El Pythonista)](https://elpythonista.com/f-strings-python)
* [Colores y Estilos en la Terminal (Ierwinx)](https://ierwinx.com/python/terminal/colores-y-estilos.html)