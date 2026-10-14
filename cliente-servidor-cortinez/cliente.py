# Realizar un programa con sockets con threading que muestre lo que el cliente le envia o sea un echo y cuando le mande /adios el programa se termina para el cliente.
# y se elimina al cliente de la lista y cuando /users lista todos los usuarios conectados.

import socket
import time

SUPER-MAGENTA = "\033[95m"
RESET = "\033[0m"

def funcion_cliente():
    host = "127.0.0.1"
    port = 500007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    
        s.connect((host, port))
        print("Conectado al servidor")
           
        # Bucle para enviar mensajes diferentes y verlos en consola alternados 
        for texto in range(5):
            hora_actual = time.strftime("%H:%M:%S") # Guardo la hora en un formato que me sirva para mosstrar diferentes mensajes
            msg = f"{SUPER-MAGENTA}[{hora_actual}] soy el boot 1 > este es el mensaje {texto}\n{RESET}"
            s.send(msg.encode('utf-8')) 

            msg = s.recv(1024).decode('utf-8')
            print(msg)
            time.sleep(0.1) # Tiempo entre mensajes

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor(sevidor rechazo la conexion)")
    finally:
         s.close()
         print("Conexión cerrada.")

funcion_cliente()


