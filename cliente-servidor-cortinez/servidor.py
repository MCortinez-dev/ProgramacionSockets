# Realizar un programa con sockets con threading que muestre lo que el cliente le envia o sea un echo y cuando le mande /adios el programa se termina para el cliente.
# y se elimina al cliente de la lista y cuando /users lista todos los usuarios conectados.

import socket
import threading as th

def manejar_cliente(conn, addr, lista_clientes):
    print(f"\n[NUEVA CONEXIÓN] {addr} conectado.")
    
    conectado = True
    while conectado:
        try:
            # Recibe el mensaje
            mensaje = conn.recv(1024).decode('utf-8') # Recibe hasta 1024 bytes de datos desde el socket del cliente y los decodifica de bytes a texto (string)
            if not mensaje:
                break
            
            print(f"[{addr}] dice: {mensaje}")
            
            # Eco: devuelve el mensaje al cliente
            conn.send(f"Eco: {mensaje}".encode('utf-8'))
            
        except ConnectionResetError: #Captura error de desconexión
            break

    # Al terminar la conexión
    conn.close()
    # Elimina este socket de la lista global de clientes
    lista_clientes.remove(conn)
    print(f"\n[DESCONEXIÓN] {addr} se ha ido.")
    print(f"[CLIENTES ACTIVOS] {len(lista_clientes)}")

def servidorbase():
    host = '127.0.0.1' # la ip del servidor en localhost
    port = 500007
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creo el socket  ipv4(AF_INET) y tcp(SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # para permitir la reutilizacion de la direccion
      
    try:
        servidor.bind((host, port)) # enlazo el socket con la ip y el puerto
        servidor.listen(5) # escucha 5 peticiones en cola de espera
        print(f'El servidor esta escuchando en {host}:{port}')
        
        
        clientes_activos = []
        print("[INICIO] Servidor escuchando en el puerto 5050...")

        while True:
            conn, addr = server.accept()
            clientes_activos.append(conn) # Se agrega cliente a la lista
            
            # Crear hilo para el nuevo cliente
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr, clientes_activos))
            hilo.start()
            
            print(f"[CLIENTES ACTIVOS] {len(clientes_activos)}")

    except KeyboardInterrupt:
        print('Servidor detenido')
    except ConnectionResetError:
        print('Conexion cerrada por el cliente')
    finally:
        servidor.close()

servidorbase()