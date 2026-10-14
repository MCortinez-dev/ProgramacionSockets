# Realizar un programa con sockets con threading que muestre lo que el cliente le envia o sea un echo y cuando le mande /adios el programa se termina para el cliente.
# y se elimina al cliente de la lista y cuando /users lista todos los usuarios conectados.

import socket
import threading as th

def manejar_cliente(conn, addr, lista_clientes):
    print(f"\n[NUEVA CONEXIÓN] {addr} conectado.")

    VERDE = "\033[3;32m"
    RESET = "\033[0m"
    
    conectado = True
    while conectado:
        try:
            # Recibe el mensaje
            mensaje = conn.recv(1024).decode('utf-8') # Recibe hasta 1024 bytes de datos desde el socket del cliente y los decodifica de bytes a texto (string)
            if not mensaje:
                break

            # Intento evitar error ConnectionAbortedError: [WinError 10053]
            if mensaje.strip().lower() == "/adios":
                print(f"{VERDE}[{addr}] solicitó desconexión (/adios).{RESET}")
                conn.send("¡Adiós! Cerrando conexión...".encode('utf-8'))
                break

            if mensaje.strip().lower() == "/users":
                respuesta = f"{VERDE}[SERVIDOR] Hay {len(lista_clientes)} clientes conectados.{RESET}"
                conn.send(respuesta.encode('utf-8'))
                continue
            
            print(f"\n{VERDE}[{addr}] dice:\n {mensaje}{RESET}")
            
            # Eco: devuelve el mensaje al cliente
            conn.send(f"{VERDE}Eco: {mensaje}{RESET}".encode('utf-8'))
            
        except ConnectionResetError: #Captura error de desconexión
            break

    # Al terminar la conexión
    conn.close()
    # Elimina este socket de la lista global de clientes
    if conn in lista_clientes:
        lista_clientes.remove(conn)
    print(f"\n[DESCONEXIÓN] {addr} se ha ido.")
    print(f"[CLIENTES ACTIVOS] {len(lista_clientes)}")

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
            
            print(f"{VERDE}[CLIENTES ACTIVOS] {len(clientes_activos)}{RESET}")

    except KeyboardInterrupt:
        print('Servidor detenido')
    except ConnectionResetError:
        print(f'{VERDE}Conexion cerrada por el cliente{RESET}')
    finally:
        servidor.close()

servidorbase()