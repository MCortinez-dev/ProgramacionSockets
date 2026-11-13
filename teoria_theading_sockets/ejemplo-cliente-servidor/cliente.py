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