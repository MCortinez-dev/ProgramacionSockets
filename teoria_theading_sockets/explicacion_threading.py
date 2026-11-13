import threading
import time

def tarea_pesada(nombre, duracion):
    """
    Simula una tarea que toma tiempo (como descargar un archivo o procesar datos).
    """
    print(f"  [Hilo {nombre}] Iniciando tarea (durará {duracion}s)...")
    time.sleep(duracion)
    print(f"  [Hilo {nombre}] ¡Tarea terminada!")

def demo_secuencial():
    print("\n--- Ejecución Secuencial (Sin Threads) ---")
    inicio = time.time()
    
    # Se ejecuta una tras otra
    tarea_pesada("A", 2)
    tarea_pesada("B", 2)
    
    fin = time.time()
    print(f"Tiempo total secuencial: {fin - inicio:.2f} segundos")

def demo_con_threads():
    print("\n--- Ejecución Concurrente (Con Threads) ---")
    inicio = time.time()
    
    # 1. Creamos los objetos Thread
    # target: la función que queremos ejecutar
    # args: los argumentos que recibe esa función
    hilo1 = threading.Thread(target=tarea_pesada, args=("A", 2))
    hilo2 = threading.Thread(target=tarea_pesada, args=("B", 2))
    
    # 2. Iniciamos los hilos con .start()
    # Esto le dice al Sistema Operativo que empiece a ejecutarlos en paralelo
    hilo1.start()
    hilo2.start()
    
    # El programa principal sigue corriendo aquí...
    print("  [Principal] Yo sigo trabajando mientras los hilos corren...")
    
    # 3. Usamos .join() para esperar a que terminen antes de calcular el tiempo total
    # Sin .join(), el programa principal llegaría al final antes que los hilos
    hilo1.join()
    hilo2.join()
    
    fin = time.time()
    print(f"Tiempo total con threads: {fin - inicio:.2f} segundos")

if __name__ == "__main__":
    print("EXPLICACIÓN DE THREADING")
    print("========================")
    print("Los hilos permiten que tu programa haga varias cosas al 'mismo tiempo'.")
    
    demo_secuencial()
    demo_con_threads()
    
    print("\nCONCLUSIÓN:")
    print("En la versión secuencial tardamos 4 segundos (2+2).")
    print("En la versión con threads tardamos solo 2 segundos, porque ambos corrieron a la vez.")
