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
        print("Conectado al servidor")
                  
        # Valido al usuario - lado cliente
        valido_usuario = s.recv(1024).decode('utf-8')
        print(valido_usuario) # Recivo la pregunta
        usuario_tipeado = input("> ")
        s.send(usuario_tipeado.encode('utf-8')) # Contesto

        # Valido la clave - lado cliente
        valido_clave = s.recv(1024).decode('utf-8')
        print(valido_clave) # Recivo la pregunta
        clave_tipeada = input("> ")
        s.send(clave_tipeada.encode('utf-8')) # Contesto

        #Respuesta del servidor sobre las credenciales
        respuesta_login = s.recv(1024).decode('utf-8')
        print(respuesta_login)

        # Lee la respuesta y se fija si estan mal las credenciales
        if "incorrectos" in respuesta_login or "rechazada" in respuesta_login:
            return

        # Charla con servidor
        while True:
            hora_actual = time.strftime("%H:%M:%S") # Guardo la hora en un formato que me sirva para mosstrar diferentes mensajes
            cosas_tipeadas = input("> ")

            # Para salir
            if cosas_tipeadas.strip().lower() == "/adios":
                s.send(cosas_tipeadas.encode('utf-8'))
                despedida = s.recv(1024).decode('utf-8')
                print(despedida)
                break

            # Para recivir lista usuarios conectados
            if cosas_tipeadas.strip().lower() == "/users":
                s.send(cosas_tipeadas.encode('utf-8'))
                respuesta_servidor = s.recv(1024).decode('utf-8')
                print(f"\n{respuesta_servidor}\n")
                continue

            msg = f"{CIAN}[{hora_actual}] Soy un cliente que ingresa datos por el teclado [para dejar de escribir = /adios] > este es el mensaje =>>> {RESET} {SUPERMAGENTA}{cosas_tipeadas}\n{RESET}"
            s.send(msg.encode('utf-8'))             

            # Recibo respuesta servidor
            recibido = s.recv(1024).decode('utf-8')
            print(recibido)


    except ConnectionRefusedError:
        print("No se pudo conectar al servidor(sevidor rechazo la conexion)")
    finally:
         s.close()
         print("Conexión cerrada.")

funcion_cliente()