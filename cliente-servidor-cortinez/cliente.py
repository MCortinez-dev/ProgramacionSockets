# Realizar un programa con sockets con threading que muestre lo que el cliente le envia o sea un echo y cuando le mande /adios el programa se termina para el cliente.
# y se elimina al cliente de la lista y cuando /users lista todos los usuarios conectados.

import socket

def funcion_cliente():
    host = "127.0.0.1" # es la ip del servidor
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creo el socket
    try:
    
        s.connect((host, port)) # conecto al servidor
        print("Conectado al servidor")

        while True:
            msg = input(">")   # ingreso el mensaje por teclado
            s.send(msg.encode('utf-8')) # mando el mensaje
            if msg.strip().lower() == "/adios":
                break
            msg = s.recv(1024).decode('utf-8')
            print(msg)

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor(sevidor rechazo la conexion)")
    finally:
         s.close()
         print("Conexión cerrada.")
funcion_cliente()

# Bibliofrafia
# https://docs.python.org/3/library/socket.html
# https://docs.python.org/3/library/socketserver.html#module-socketserver
# https://docs.python.org/3/library/threading.html
