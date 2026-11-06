import socket
import time

SUPERMAGENTA = "\033[1;4;95m" # negrira - subrayado - magenta brillante
CIAN = "\033[36m"
RESET = "\033[0m"

def funcion_cliente():
    host = "127.0.0.1"
    port = 49152
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.connect((host, port))
        usuarioCliente = "alumno2006"
        claveCliente = "re23@58py92"

        s.send(usuarioCliente.encode('utf-8'))
        s.send(claveCliente.encode('utf-8'))
        verificacion_logueo = s.recv(1024).decode('utf-8')

        if verificacion_logueo:
                
                try:
                    print("Conectado al servidor")
                    
                    # Bucle para enviar mensajes diferentes y verlos en consola alternados 
                    while True:
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

                        msg = f"{CIAN}[{hora_actual}] Soy un cliente que ingresa datos por el teclado [para dejar de escribir = /adios] > este es el mensaje =>>> {RESET} {SUPERMAGENTA}{cosas_tipeadas}\n{RESET}"

                        s.send(msg.encode('utf-8'))             

                        recivido = s.recv(1024).decode('utf-8')
                        print(recivido)

                except ConnectionRefusedError:
                    print("No se pudo conectar al servidor(sevidor rechazo la conexion)")
        else:


    
    except:
         








    except:


    finally:
         s.close()
         print("Conexión cerrada.")

funcion_cliente()