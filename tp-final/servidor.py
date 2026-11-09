#Importar librerias a usar
import socket
import threading as th # Multihilos

# Base de datos
import mysql.connector # Base de datos
from mysql.connector import Error
import os # Nueva forma que encontre importa cosas del sistema operativo (probar)
from dotenv import load_dotenv  # pip install python-dotenv

# 
import requests

#-----------------------------------------------------------------------------------------------------
# Cargo variables entorno
load_dotenv()

#-----------------------------------------------------------------------------------------------------
# Funsion conectar DB
def conectar_DB():
    try:
        conexion = mysql.connector.connect(
            host = os.getenv("DB_HOST", "localhost"),
            port = int(os.getenv("DB_PORT", 3306)),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME"),
            charset = "utf8mb4"
        )
        return conexion 
    
    except Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu nombre de usuario o contraseña")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(f"Error: {err}")

# ----------------------------------------------------------------------------------------
# Funsión Manejar Cliente
def manejar_cliente(conn, addr, lista_clientes):

    # Aviso que hay una conexíon establecida
    print(f"\n[NUEVA CONEXIÓN] {addr} conectado.")
    
    # Conecto a la base de datos
    db_up = conectar_DB()
    if db_up:
        print(f"La base de datos existe y la encontramos a traves del puerso 3306")
    else:
        print(f"Hay un prblema en la base de datos")

    VERDE = "\033[3;32m"
    RESET = "\033[0m"
    
    conectado = True
    while conectado:
        try:
            # Le pregunto el usuario y contraseña
            conn.send("Hola ¿Cual es tu nombre de usuario?".encode('utf-8'))
            usuario_cliente = conn.recv(1024).decode('utf-8')
            if not usuario_cliente:
                break

            conn.send("Ahora decime ¿Cual es tu contraseña?".encode('utf-8'))
            usuario_clave = conn.recv(1024).decode('utf-8')
            if not usuario_clave:
                break

            # Si hay una base de datos levantada, entoces hago la consulta para comparar
            if db_up:
                consulta = db_up.cursor()
                
                # Limpio el código sacando el try
                consulta.execute("SELECT * FROM usuarios WHERE nombre = %s AND clave_encrip = %s", (usuario_cliente, usuario_clave))
                consulta_respuesta = consulta.fetchone()  # Verifico si pudo realizar la consulta
                
                # Si se ejecuto la consulta significa que habia un usuario y contraseña iguales en la Base de Datos
                if consulta_respuesta:
                    print(f'{usuario_cliente} tu usuario y contraseña son correctos')
                    # Recibe el mensaje luego de validar y se queda charlando
                    conn.send("¡Ya podemos charlas! Bienvenido\n".encode('utf-8'))
                    
                    while conectado:
                        mensaje = conn.recv(1024).decode('utf-8') # Recibe hasta 1024 bytes de datos desde el socket del cliente y los decodifica de bytes a texto (string)
                        if not mensaje:
                            break

                        # Intento evitar error ConnectionAbortedError: [WinError 10053]
                        if mensaje.strip().lower() == "/adios":
                            print(f"{VERDE}[{addr}] solicitó desconexión (/adios).{RESET}")
                            try:
                                conn.send("¡Adiós! Cerrando conexión...".encode('utf-8'))
                            except:
                                pass # Intento evitar error ConnectionAbortedError: [WinError 10038] - no sirvió
                            break

                        if mensaje.strip().lower() == "/users":
                            respuesta = f"{VERDE}[SERVIDOR] Hay {len(lista_clientes)} clientes conectados.{RESET}"
                            conn.send(respuesta.encode('utf-8'))
                            continue

                        # Zona invocación poder obscuro de las APIs ?? 
                        
                        print(f"\n{VERDE}[{addr}] dice:\n {mensaje}{RESET}")
                        # Eco: devuelve el mensaje al cliente
                        conn.send(f"{VERDE}Eco: {mensaje}{RESET}".encode('utf-8'))

                else:
                    print(f'Usuario o contraseña incorrectos')
                    conn.send("Usuario o contraseña incorrectos. Conexión rechazada.\n".encode('utf-8'))
                    break
        
            else:
                print("Problema con la DB")
                break

        except Exception as e:
            print(f"Error inesperado en el cliente: {e}")

        # Al terminar la conexión
        conn.close()
        # Elimina este socket de la lista global de clientes
        if conn in lista_clientes:
            lista_clientes.remove(conn)
        print(f"\n[DESCONEXIÓN] {addr} se ha ido.")
        print(f"[CLIENTES ACTIVOS] {len(lista_clientes)}")

#----------------------------------------------------------------------------------------------------------------------------
# Funcion servidor (invoca el poder de las otras funciones)
def servidorbase():
    host = '127.0.0.1' # la ip del servidor en localhost
    port = 49152
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creo el socket  ipv4(AF_INET) y tcp(SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # para permitir la reutilizacion de la direccion

    VERDE = "\033[3;32m"
    RESET = "\033[0m"    
      
    try:
        servidor.bind((host, port)) # enlazo el socket con la ip y el puerto
        servidor.listen(10) # escucha 5 peticiones en cola de espera
        print(f'El servidor esta escuchando en {host}:{port}')

        clientes_activos = []
        print(f"{VERDE}[INICIO] Servidor escuchando en el puerto 49152...{RESET}")

        while True:
            conn, addr = servidor.accept()
            clientes_activos.append(conn) # Se agrega cliente a la lista
            
            # Crear hilo para el nuevo cliente
            hilo = th.Thread(target=manejar_cliente, args=(conn, addr, clientes_activos))
            hilo.start()

            # Intente agregar join pero me trabó todo
            # hilo.join()
            
            print(f"{VERDE}[CLIENTES ACTIVOS] {len(clientes_activos)}{RESET}")

    except KeyboardInterrupt:
        print('Servidor detenido')
    except ConnectionResetError:
        print(f'{VERDE}Conexion cerrada por el cliente{RESET}')
    finally:
        servidor.close()

servidorbase()