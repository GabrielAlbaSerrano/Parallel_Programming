"""

PRÁCTICA 1 (PARTE OBLIGATORIA) - PRPA:
GABRIEL ALBA SERRANO

"""

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
from random import random, sample


N = 5 #cantidad de números que producen los productores
NPROD = 3 #número de productores

def delay(factor = 3):
    sleep(random()/factor)


def add_data(storage, index, pid, data, mutex):
    mutex.acquire()
    try:
        storage[index.value] = data
        delay()
        index.value = index.value + 1
    finally:
        mutex.release()


def get_data(storage, index, mutex):
    mutex.acquire()
    try:
        data = storage[0]
        index.value = index.value - 1
        delay()
        for i in range(index.value):
            storage[i] = storage[i + 1]
        storage[index.value] = -2
    finally:
        mutex.release()
    return data


def producer(storage, index, empty, non_empty, mutex):
    # Generamos una lista de numeros aleatorios no negativos en orden creciente
    # He elegido N**2 como cota superior del intervalo, pero bastaría coger
    # una cota superior mayor que 0
    nums = sorted( sample(range(0,N**2), N) )
    # Añadimos cada número al almacen correspondiente
    for n in nums:
        print (f"producer {current_process().name} produciendo")
        delay()
        empty.acquire()
        add_data(storage, index, int(current_process().name.split('_')[1]),
                 n, mutex)
        non_empty.release()
        print (f"producer {current_process().name} almacenado {n}")
    # Cuando el proceso acaba de producir, produce un -1, es decir, añade un -1
    # al almacen
    print (f"producer {current_process().name} terminando")
    delay()
    empty.acquire()
    add_data(storage, index, int(current_process().name.split('_')[1]),
             -1, mutex)
    non_empty.release()
    print (f"producer {current_process().name} finalizado")
    
    
def consumer(storagelst, indexlst, emptylst, non_emptylst, mutexlst):
    result = []
    for i in range(NPROD):
        non_emptylst[i].acquire()
    
    # Iteramos hasta que todos los primeros elementos del almacén de cada productor
    # son negativos, es decir, los valores de cada almacén son -1 o -2 (indicando que el proceso
    # de producir números positivos ha terminado o que en esa posición el almacén está vacío)
    while any(storagelst[i][0] >= 0 for i in range(NPROD)):

        # Creamos la lista l que consiste en el primer término de cada productor,
        # es decir, el menor que ha producido y que sigue en el almacen.
        l = [storagelst[i][0] for i in range(NPROD)]

        # Definimos m como el menor numero no negativo de la lista l, tiene que ser
        # no negativo porque el -1 y el -2 indican, respectivamente, que se ha terminado
        # de producir y que el almacen esta vacio (no son producciones como tal)
        m = min(filter(lambda x : x >= 0, l))
        ind = l.index(m)

        # Extraemos del almacén dicho elemento m y lo añadimos a la lista result
        emptylst[ind].release()
        dato = get_data(storagelst[ind], indexlst[ind], mutexlst[ind])
        non_emptylst[ind].acquire()
        result.append(dato)
        delay()
        
    print('La lista ordenada por un merge concurrente es: ' + str(result))


def main():
    storagelst = [Array('i', N) for i in range(NPROD)]
    indexlst = [Value('i', 0) for i in range(NPROD)]
    
    for i in range(NPROD):
        for j in range(N):
            storagelst[i][j] = -2
        print ("El almacen inicial del productor numero", i, "es", 
               storagelst[i][:], " , con indice", indexlst[i].value)
    
    # Creamos listas de semaforos que seran manejados unicamente por sus
    # respectivos productores
    non_emptylst = [Semaphore(0) for i in range(NPROD)]
    emptylst = [Semaphore(N) for i in range(NPROD)]
    mutexlst = [Lock() for i in range(NPROD)]
    
    prodlst = [ Process(target = producer,
                        name = f'prod_{i}',
                        args = (storagelst[i], indexlst[i], emptylst[i], 
                              non_emptylst[i], mutexlst[i]))
                for i in range(NPROD) ]
    
    # El proceso merge maneja todos los semáforos
    merge =  [ Process(target = consumer, name = f'consumer', 
                        args = (storagelst, indexlst, emptylst, non_emptylst, 
                                mutexlst)) ]
                
    for p in prodlst + merge:
        p.start()

    for p in prodlst + merge:
        p.join()


if __name__ == '__main__':
    main()