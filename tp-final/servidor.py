#Importar librerias a usar
import socket # The socket module provides low-level networking interface for creating network connections.
import threading as th # Multihilos

# Base de datos
import mysql.connector # Base de datos
from mysql.connector import Error
import os # usar funcionalidades dependientes del sistema operativo (es muy grande evaluar importar solo un modulo)
from dotenv import load_dotenv  # pip install python-dotenv

# The requests module allows you to send HTTP requests using Python.
import requests

# MOdulo de tiempo
import time

#-----------------------------------------------------------------------------------------------------
# Cargo variables entorno
load_dotenv()

#-----------------------------------------------------------------------------------------------------
# Configuración de colores para la consola del servidor
VERDE = "\033[32m"
ROJO = "\033[31m"
RESET = "\033[0m"

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
            print(f"{ROJO}[DB ERROR] Usuario o contraseña incorrectos.{RESET}")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print(f"{ROJO}[DB ERROR] La base de datos especificada no existe.{RESET}")
        else:
            print(f"{ROJO}[DB ERROR] {err}{RESET}")

# ----------------------------------------------------------------------------------------
# Funsión Manejar Cliente
def manejar_cliente(conn, addr, lista_clientes):

    # Aviso que hay una conexíon establecida
    print(f"\n{VERDE}[NUEVA CONEXIÓN] {addr} conectado.{RESET}")
    
    # Conecto a la base de datos
    db_up = conectar_DB()
    if db_up:
        print(f"{VERDE}[DB OK]La base de datos existe y la encontramos a traves del puerto 3306{RESET}")
    else:
        print(f"{ROJO}[DB ALERTA] Problema al conectar con la base de datos.{RESET}")
    
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
                    print(f"{VERDE}[AUTENTICACIÓN] {usuario_cliente} validado correctamente.{RESET}")
                    # Recibe el mensaje luego de validar y se queda charlando
                    conn.send("¡Ya podemos charlas! Bienvenido\n".encode('utf-8'))

                    # Manejo de comandos
                    while conectado:
                        # Recibo mensajes del cliente
                        mensaje = conn.recv(1024).decode('utf-8') # Recibe hasta 1024 bytes de datos desde el socket del cliente y los decodifica de bytes a texto (string)
                        if not mensaje:
                            break

                        # Como hay muchos comandos, limpio el mensaje una sola vez. Saca espacios en los extremos y pone en minúscula
                        cmd = mensaje.strip().lower()

                        # Cliente X manda de su consola a todos
                        if cmd.startswith("/todos"):
                            partes = mensaje.split(maxsplit=1) # Separa por espacios, para ver si me lee el nombre de usuario que busco

                            # Si tiene algo escrito para todos lo agarro, guardo y envío
                            if len(partes) > 1:
                                mensaje_a_todos = partes[1]
                                texto_a_enviar = f"\n[MENSAJE GLOBAL de {usuario_cliente}]: {mensaje_a_todos}\n"
                            else:
                                texto_a_enviar = f"\n[MENSAJE GLOBAL de {usuario_cliente}]: (vacío)\n" # Si mandó solo algo vacio
                            
                            # PRobar poninedo clientes boots si los recorre y les envia el mensaje
                            for cliente_socket in lista_clientes.copy():
                                try:
                                    cliente_socket.sendall(texto_a_enviar.encode('utf-8'))
                                except:
                                    pass                            
                            continue

                        # Comandos interactuar API de GitHub
                        if cmd.startswith("/repos") or cmd.startswith("/followers"):
                            partes = cmd.split() # Separa por espacios, para ver si me lee el nombre de usuario que busco
                            tipo_comando = partes[0] # "/repos"
                            
                            # Cuando escriba un usuario va a haber dos partes en el mensaje
                            if len(partes) > 1:
                                usuario_seleccionado = partes[1]
                            else:
                                usuario_seleccionado = "" # Si mandó solo /repos vacío

                            # Inicio la funcion correspondiente con todos los argumentos
                            github(tipo_comando, conn, db_up, usuario_seleccionado)
                            continue

                        # Intento evitar error ConnectionAbortedError: [WinError 10053]
                        if cmd == "/adios":
                            print(f"{VERDE}[DESCONEXIÓN SOLICITADA] {addr} ({usuario_cliente}){RESET}")
                            try:
                                conn.send("¡Adiós! Cerrando conexión...".encode('utf-8'))
                            except:
                                pass # Intento evitar error ConnectionAbortedError: [WinError 10038] - no sirvió
                            break

                        if cmd == "/usuarios":
                            respuesta = f"[SERVIDOR] Hay {len(lista_clientes)} clientes activos conectados."
                            conn.send(respuesta.encode('utf-8'))
                            continue

                        if cmd == "/hora":
                            hora_actual = time.strftime("%H:%M:%S") # Guardo la hora en un formato que sirva para verse en la respuesta
                            respuesta = f"{VERDE}[SERVIDOR] La hora actual del servidor es {hora_actual}.{RESET}"
                            conn.send(respuesta.encode('utf-8'))
                            continue

                else:
                    print(f"{ROJO}[AUTENTICACIÓN FALLIDA] Credenciales incorrectas para '{usuario_cliente}'.{RESET}")
                    conn.send("Usuario o contraseña incorrectos. Conexión rechazada.\n".encode('utf-8'))
                    break
        
            else:
                conn.send("Error interno: Sin conexión a la base de datos.\n".encode('utf-8'))
                break

        except Exception as e:
            print(f"{ROJO}[ERROR EN CLIENTE] {e}{RESET}")
            break

        # Al terminar la conexión
        try:
            conn.close()
        except:
            pass
        
        if conn in lista_clientes:
            lista_clientes.remove(conn)
        
        print(f"\n{VERDE}[DESCONEXIÓN] {addr} se ha ido. Clientes activos: {len(lista_clientes)}{RESET}")
#----------------------------------------------------------------------------------------------------------------------------
# Funcion utiliza request para manejar comandos de API, almacena los resultados en MySQL.
def github(comando, conn, db_up, usuario_seleccionado):

    try:
        # Si el usuario vino vacío o no lo pusieron al lado
        if not usuario_seleccionado:
            conn.send("Error: Debe ingresar un usuario de GitHub (Ej: /repos octocat).\n".encode('utf-8'))
            return    
        
        # Si no hay base de datos levantada
        if not db_up:
            conn.send("Error: No hay conexión con la base de datos.\n".encode('utf-8'))
            return

        # Preparo puente SQL
        cursor = db_up.cursor()

        # Para resolver problema 403, arme una token de github
        token_github = os.getenv("GITHUB_TOKEN")

        # Agrego user agente en header: All API requests must include a valid User-Agent header. The User-Agent header identifies the user or application that is making the request.
        headers = {
            'X-GitHub-Api-Version': '2026-03-10',
            'User-Agent': 'MCortinez-Project',
            'Authorization': f'Bearer {token_github}'
        }

        # --- Comando /repos ---
        if comando == "/repos":
            # URLs de la API, agrego el usuario seleccionado
            url_repo = f'https://api.github.com/users/{usuario_seleccionado}/repos'

            # Tomo de la url armada antes la info de los repos que tiene. La docu actual pide un header
            datos_url_repo = requests.get(url_repo, headers=headers)

            # Si reposnde peticion procesada correctamente (200)
            if datos_url_repo.status_code == 200:
                # Guardo el json que traje con el GET
                repositorios = datos_url_repo.json()

                # Parte de arriba intento de tabla guardada para mostrar en consola
                confirmacion_guardado = f"\n--- REPOSITORIOS DE: {usuario_seleccionado} ---\n"

                # Recorrer cada repositorio, tomar datos e insertarlos en la base de datos
                for repo in repositorios:
                    owner = repo.get('owner', {}).get('login', usuario_seleccionado) # para acceder a owner la consulta es diferente
                    name = repo.get('name')
                    html_url = repo.get('html_url')
                    stargazers = repo.get('stargazers_count', 0)
                    created_at = repo.get('created_at', '')
                    updated_at = repo.get('updated_at', '')
                    
                    # Muestro lo que se encontro y luego se guardo
                    print(f"Guardando: {name} ({html_url}) (Stars: {stargazers})")

                    # Esto inserta en la tabla los valores
                    insertar_repositorio = f" INSERT INTO repositorios (owner, name, html_url, stargazers_count, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
                    # Ejecuto consulta pasandoles los valores que estaban con signo de intrrrogacion
                    cursor.execute(insertar_repositorio, (owner, name, html_url, stargazers, created_at, updated_at))
                    db_up.commit() # saves the changes to the database transaction.
                    confirmacion_guardado += f"|| {name}\n | {html_url}\n > Stars:{stargazers} > Actualizado: {updated_at}\n \n"
                
                #conn.send(f"El repositorio '{usuario_seleccionado}' y sus datos se guardaron en la base de datos.\n".encode('utf-8'))
                conn.send(confirmacion_guardado.encode('utf-8'))

            else:
                conn.send(f"Error al consultar repositorios: (CÓDIGO HTTP:{datos_url_repo.status_code})\n".encode('utf-8'))


        elif comando == "/followers": # Cuando usa el otro comando
            # URL followers
            url_followers = f'https://api.github.com/users/{usuario_seleccionado}/followers'
            
            # Teniendo muchas variables configuradas arriba le inicio la consulta
            datos_url_followers = requests.get(url_followers, headers=headers)

            if datos_url_followers.status_code == 200:
                followers = datos_url_followers.json()

                #Muestreo de followers
                f_guardado = f"\n-- Seguidores de: {usuario_seleccionado} --\n"

                # Recorrer cada repositorio, tomar datos e insertarlos en la base de datos
                for f in followers:
                    owner = usuario_seleccionado
                    f_name = f.get('login')
                    f_html_url = f.get('html_url')
                    type = f.get('type')

                    # Muestro lo que se encontro y luego se guardo
                    print(f"Guardando: {f_name} ({f_html_url}) (Type: {type})")

                    # Esto inserta en la tabla los valores
                    insertar_follower = f" INSERT INTO followers (seleccionado, f_name, f_html_url, f_type) VALUES (%s, %s, %s, %s)"
                    
                    # Ejecuto consulta pasandoles los valores que estaban con signo de intrrrogacion
                    cursor.execute(insertar_follower, (owner, f_name, f_html_url, type))
                    db_up.commit() # saves the changes to the database transaction.
                    
                    f_guardado += f"|| {f_name}\n | {f_html_url}\n \n"
                
                #conn.send(f"El repositorio '{usuario_seleccionado}' y sus datos se guardaron en la base de datos.\n".encode('utf-8'))
                conn.send(f_guardado.encode('utf-8'))

            else:
                conn.send(f"Error al consultar seguidores: (CÓDIGO HTTP{datos_url_followers.status_code})\n".encode('utf-8'))                   
            
        cursor.close()

    except Exception as e:
        print(f"{ROJO}[ERROR EN MÓDULO GITHUB] {e}{RESET}")
        try:
            conn.send("Ocurrió un error interno en el servidor al procesar la API de GitHub.\n".encode('utf-8'))
        except:
            pass

#----------------------------------------------------------------------------------------------------------------------------
# Funcion servidor (invoca el poder de las otras funciones)
def servidorbase():
    host = '127.0.0.1' # la ip del servidor en localhost
    port = 49152
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creo el socket  ipv4(AF_INET) y tcp(SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # para permitir la reutilizacion de la direccion
   
    try:
        servidor.bind((host, port)) # enlazo el socket con la ip y el puerto
        servidor.listen(10) # escucha 10 peticiones en cola de espera
        
        clientes_activos = []
        print(f'El servidor esta escuchando en {host}:{port}')

        while True:
            conn, addr = servidor.accept()
            clientes_activos.append(conn) # Se agrega cliente a la lista
            
            # Crear hilo para el nuevo cliente
            hilo = th.Thread(target=manejar_cliente, args=(conn, addr, clientes_activos))
            hilo.start()
            
            print(f"{VERDE}[CLIENTES ACTIVOS] {len(clientes_activos)}{RESET}")

    except KeyboardInterrupt:
        print(f"\n{VERDE}[SERVIDOR DETENIDO] Apagando el servidor de forma segura.{RESET}")
    except ConnectionResetError:
        print(f"{ROJO}[ERROR] Conexión restablecida abruptamente.{RESET}")
    finally:
        servidor.close()

if __name__ == "__main__":
    servidorbase()