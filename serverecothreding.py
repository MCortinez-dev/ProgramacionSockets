import socket
import threading

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

def iniciar_servidor():
    # Crea el socket principal del servidor:
    # - AF_INET: Indica direcciones IPv4.
    # - SOCK_STREAM: Indica que usaremos el protocolo TCP    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enlaza el socket del servidor a una IP local y a un puerto 5050
    server.bind(('localhost', 5050)) # la privada del servidor o localhost(127.0.0.1) RFC 1122
    # servidor en "modo escucha"
    server.listen()
    
    clientes_activos = []
    print("[INICIO] Servidor escuchando en el puerto 5050...")

    while True:
        # .accept() se BLOQUEA (pausa el bucle) aquí hasta que un cliente intenta conectarse. 
        # Cuando lo hace, devuelve dos cosas: 'conn' (el canal exclusivo para hablar con ese cliente) y 'addr' (su IP y puerto)
        conn, addr = server.accept()
        clientes_activos.append(conn) # Se agrega cliente a la lista
        
        # Crear hilo para el nuevo cliente
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr, clientes_activos))
        hilo.start()
        
        print(f"[CLIENTES ACTIVOS] {len(clientes_activos)}")

if __name__ == "__main__":
    iniciar_servidor()
