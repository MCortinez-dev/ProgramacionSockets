# Realizar un programa con sockets con threading que muestre lo que el cliente le envia o sea un echo y cuando le mande /adios el programa se termina para el cliente.
# y se elimina al cliente de la lista y cuando /users lista todos los usuarios conectados.

import socket
import time

SUPERMAGENTA = "\033[1;4;95m" # negrira - fondo azul - subrayado - magenta brillante
CIAN = "\033[36m"
RESET = "\033[0m"

def funcion_cliente():
    host = "127.0.0.1"
    port = 49152
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
    
        s.connect((host, port))
        print("Conectado al servidor")
           
        # Bucle para enviar mensajes diferentes y verlos en consola alternados 
        for texto in range(5):
            hora_actual = time.strftime("%H:%M:%S") # Guardo la hora en un formato que me sirva para mosstrar diferentes mensajes
            
            cosas_tipeadas = input("> ")

            # Para salir
            if cosas_tipeadas.strip().lower() == "/adios":
                s.send(cosas_tipeadas.encode('utf-8'))
                break

            # Para recivir lista usuarios conectados
            if cosas_tipeadas.strip().lower() == "/users":
                s.send(cosas_tipeadas.encode('utf-8'))
                respuesta_servidor = s.recv(1024).decode('utf-8')
                print(f"\n{respuesta_servidor}\n")
                continue            

            msg = f"{SUPERMAGENTA}[{hora_actual}] Soy un cliente que ingresa datos por el teclado [para dejar de escribir = /adios] > este es el mensaje =>>> {RESET} {CIAN}{cosas_tipeadas}\n{RESET}"

            s.send(msg.encode('utf-8'))             

            recivido = s.recv(1024).decode('utf-8')
            print(recivido)
            # time.sleep(1.5) # Tiempo entre mensajes

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor(sevidor rechazo la conexion)")
    finally:
         s.close()
         print("Conexión cerrada.")

funcion_cliente()


