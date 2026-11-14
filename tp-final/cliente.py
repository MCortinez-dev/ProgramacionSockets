import threading as th # Para el hilo que siempre espera el mensaje de /todos
import socket
import time # Para obtener la hora

# Definición de colores para la consola
SUPERMAGENTA = "\033[1;4;95m"  # Negrita, subrayado, magenta brillante
VERDE = "\033[32m"             # Verde estándar
CIAN = "\033[36m"              # Cían
ROJO = "\033[31m"              # Rojo para errores
RESET = "\033[0m"              # Reset de formato

def escuchar_servidor(s_cliente):
    # Hilo secundario dedicado a escuchar permanentemente mensajes del servidor.
    while True:
        try:
            mensaje = s_cliente.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"\n{mensaje}")
            print("> ", end="", flush=True) # Restaura el prompt visual de la terminal, evita atascos
        except:
            break


def funcion_cliente():
    host = "127.0.0.1"
    port = 49152
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print(f"{VERDE}[CONEXIÓN] Conectado al servidor exitosamente.{RESET}")
                  
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
        #--------------------------------------------------------------------------------------------
        # Intento abrir un hilo paralelo para el mensaje a /todos, asi siempre está escuchado si trabar la charla principal
        hilo_escucha = th.Thread(target=escuchar_servidor, args=(s,), daemon=True)
        hilo_escucha.start()

        # Charla con servidor
        while True:
        
            hora_actual = time.strftime("%H:%M:%S") # Guardo la hora en un formato que me sirva para mosstrar diferentes mensajes
            cosas_tipeadas = input("> ")

            # Al aumentar los comandos guardo lo tipeado en una variable limpia
            cmd_ingresado = cosas_tipeadas.strip().lower()
            
            # Para salir
            if cmd_ingresado == "/adios":
                s.send(cosas_tipeadas.encode('utf-8'))
                despedida = s.recv(1024).decode('utf-8')
                print(f"{VERDE}{despedida}{RESET}")
                break

            # Para recibir lista usuarios conectados
            if cmd_ingresado == "/usuarios":
                s.send(cosas_tipeadas.encode('utf-8'))
                lista_conectados = s.recv(1024).decode('utf-8')
                print(f"\n{lista_conectados}\n")
                continue

            # Para recibir la hora
            if cmd_ingresado == "/hora":
                s.send(cosas_tipeadas.encode('utf-8'))
                hora_recibida = s.recv(1024).decode('utf-8')
                print(f"\n{hora_recibida}\n")
                continue

            # Para enviar mensajes a todos los conectados
            if cmd_ingresado == "/todos":
                print(f"{CIAN}¿Qué le quiere decir a todos los usuarios conectados?{RESET}")
                cliente_a_todos = input("-> ")
                mensaje_completo = f"/todos {cliente_a_todos}"
                s.send(mensaje_completo.encode('utf-8'))               
                continue

             # Para trabajar con la API
            if cmd_ingresado.startswith("/repos") or cmd_ingresado.startswith("/followers"):
                s.send(cosas_tipeadas.encode('utf-8'))

                # Muestra la respuesta que deberia variar segun el comando ingresado
                respuesta_servidor = s.recv(1024).decode('utf-8')
                print(f"\n{respuesta_servidor}\n")
                
                continue
            
            # Mensaje general - es posible que me genere errores (evaluar limpiar)
            msg = f"{CIAN}[{hora_actual}] Mensaje general =>>> {RESET}{SUPERMAGENTA}{cosas_tipeadas}{RESET}\n"
            s.send(msg.encode('utf-8'))             

            # Recibo respuesta servidor
            recibido = s.recv(1024).decode('utf-8')
            print(recibido)


    except ConnectionRefusedError:
        print(f"{ROJO}[ERROR] No se pudo conectar al servidor (conexión rechazada).{RESET}")
    finally:
         s.close()
         print("Conexión cerrada.")
         print(f"{VERDE}Conexión cerrada.{RESET}")

if __name__ == "__main__":
    funcion_cliente()