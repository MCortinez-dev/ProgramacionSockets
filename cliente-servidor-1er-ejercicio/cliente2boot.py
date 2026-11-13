import socket
import time

VERDE = "\033[32m"
RESET = "\033[0m"

def funcion_cliente():
    host = "127.0.0.1"
    port = 49152
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    
        s.connect((host, port))
        print("Conectado al servidor")
           
        # Bucle para enviar mensajes diferentes y verlos en consola alternados 
        for texto in range(100):
            hora_actual = time.strftime("%H:%M:%S") # Guardo la hora en un formato que me sirva para mosstrar diferentes mensajes
            msg = f"{VERDE}[{hora_actual}] soy el boot 2 > este es el mensaje {texto}\n{RESET}"
            s.send(msg.encode('utf-8')) 

            msg = s.recv(1024).decode('utf-8')
            print(msg)
            time.sleep(2) # Tiempo entre mensajes

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor(sevidor rechazo la conexion)")
    finally:
         s.close()
         print("Conexión cerrada.")

funcion_cliente()