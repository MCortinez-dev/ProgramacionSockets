# Realizar un programa con sockets con threading que muestre lo que el cliente le envia o sea un echo y cuando le mande /adios el programa se termina para el cliente.
# y se elimina al cliente de la lista y cuando /users lista todos los usuarios conectados.

import socket

def servidorbase():
    host = '127.0.0.1' # la ip del servidor en localhost
    port = 12345
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creo el socket  ipv4(AF_INET) y tcp(SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # para permitir la reutilizacion de la direccion
      
    try:
        servidor.bind((host, port)) # enlazo el socket con la ip y el puerto
        servidor.listen(5) # escucha 5 peticiones en cola de espera
        print(f'El servidor esta escuchando en {host}:{port}')
        while True:
            conexion, direccion = servidor.accept()
            print(f'Conexion establecida con {direccion}')
            conexion.send('Bienvenido al servidor'.encode('utf-8'))
            while True:
                mensaje = conexion.recv(1024).decode('utf-8')
                if not mensaje:
                    break
                print(f'Mensaje recibido: {mensaje}')    
                conexion.send(f'Mensaje recibido: {mensaje}'.encode('utf-8'))
            
            conexion.close()
    except KeyboardInterrupt:
        print('Servidor detenido')
    except ConnectionResetError:
        print('Conexion cerrada por el cliente')
    finally:
        servidor.close()

servidorbase()