
# Ejemplo de uso de hilos
# threading es una libreria de python para manejar hilos de ejecucion
# opciones para multiproceso en python
# multiprocessing usa todos los nucleos(cores) del procesador
# selector, permite manejar multiples sockets complejos mas conexiones  con mas complejidad
# asyncio permite manejar multiples sockets complejos mas conexiones  con mas complejidad pero es la libreria mas nueva, es un poco mas dificil de entender



import threading as th  # Importa el módulo threading para manejar hilos y lo rebautiza como 'th'
import time  # Importa el módulo time para poder usar funciones de pausa (sleep)

def hilo1():  # Define la función que se ejecutará en paralelo dentro del primer hilo
    for i in range(5):  # Inicia un bucle que se repetirá 5 veces (i de 0 a 4)
        print("Hilo 1")  # Imprime en consola el texto "Hilo 1"
        time.sleep(0.1)  # Pausa la ejecución de este hilo específico durante 0.1 segundos
        
def hilo2():  # Define la función que se ejecutará en paralelo dentro del segundo hilo
    for i in range(5):  # Inicia un bucle que se repetirá 5 veces (i de 0 a 4)
        print("Hilo 2")  # Imprime en consola el texto "Hilo 2"
        time.sleep(0.2)  # Pausa la ejecución de este hilo específico durante 0.2 segundos
        
t1 = th.Thread(target=hilo1)  # Crea un objeto de tipo Thread (t1) asignándole la función 'hilo1' como su tarea
t2 = th.Thread(target=hilo2)  # Crea un objeto de tipo Thread (t2) asignándole la función 'hilo2' como su tarea

t1.start()  # Inicia formalmente la ejecución del hilo 1 en segundo plano
t2.start()  # Inicia formalmente la ejecución del hilo 2 en segundo plano

t1.join()  # Detiene/espera en el hilo principal hasta que el hilo 1 termine por completo
t2.join()  # Detiene/espera en el hilo principal hasta que el hilo 2 termine por completo

for i in range(5):  # Una vez que terminan los hilos, inicia un bucle en el proceso principal que corre 5 veces
    print("Proceso principal:")  # Imprime en consola "Proceso principal:" en cada iteración

print("Programa finalizado")  # Imprime el mensaje final una vez que todo el flujo anterior ha concluido


