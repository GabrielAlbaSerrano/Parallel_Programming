# Implementation of a concurrent merge algorithm:

- We have NPROD processes that generate non-negative numbers in ascending order. When a process finishes generating, it produces a -1. Each process stores the value in a shared variable with the consumer, where a -2 indicates that the storage is empty.

- There is a merge process that takes the generated numbers and stores them in ascending order in a single list (or array). The process must wait for the producers to have an item ready and then insert the smallest of them.

- There are three lists of semaphores where each producer handles only its own semaphores for its data, and the merge process handles all the semaphores.

i. **emptylst**: This list stores Semaphore-type semaphores that represent the availability of empty spaces in the storage. Each producer has its semaphore in this list. The number of semaphores in emptylst is equal to the number of producers (NPROD). Each semaphore is initialized with a value N, which is the total number of numbers that that producer will produce. This indicates that there are initially spaces available for producers to store numbers.

ii. **non_emptylst**: This list stores Semaphore-type semaphores that represent the availability of elements in the storage. Each producer has its semaphore in this list. The number of semaphores in non_emptylst is equal to the number of producers (NPROD). Each semaphore is initialized with a value of 0, indicating that there are initially no elements available to retrieve in each storage.

iii. **mutexlst**: This list stores Lock-type mutexes that are used to achieve mutual exclusion when accessing the storages. Each producer has its mutex in this list. The number of mutexes in mutexlst is equal to the number of producers (NPROD). Each mutex is used to ensure that only one producer accesses a storage at a time, ensuring consistency of shared data and mutual exclusion.

- OPTIONAL: Implementation with the addition of a fixed-size buffer, where producers place values in the buffer. The main differences compared to the previous implementation are:

  i. **emptylst**: This list stores BoundedSemaphore-type semaphores that represent the availability of empty spaces in the buffer storages. Each producer has its semaphore in this list. The number of semaphores in emptylst is equal to the number of producers (NPROD). Each semaphore is initialized with a value equal to the buffer's capacity (K), indicating that there are initially spaces available for producers to store numbers.

  ii. In the `add_data` function, it's necessary to wait for the index value of the respective process to be less than K, as otherwise, it would access a position in the storage that doesn't exist.

--------------------------------------

# Implementación de un algoritmo merge concurrente:

- Tenemos NPROD procesos que producen números no negativos de forma creciente. Cuando un proceso acaba de producir, produce un -1. Cada proceso almacena el valor almacenado en una variable compartida con el consumidor, un -2 indica que el almacén está vacío.

- Hay un proceso merge que toma los números producidos y los almacena de forma creciente en una única lista (o array). El proceso debe esperar a que los productores tengan listo un elemento e introducir el menor de ellos.

- Hay 3 listas de semáforos tal que cada productor solo maneja sus semáforos para sus datos y el proceso merge maneja todos los semáforos.

  i. emptylst: Esta lista almacena los semáforos de tipo Semaphore que representan la disponibilidad de espacios vacíos en los almacenes. Cada productor tiene su propio semáforo en esta lista. El número de semáforos en emptylst es igual al número de productores (NPROD). Cada semáforo se inicializa con un valor N, igual al número total de números que ese productor va a producir, lo que indica que inicialmente hay espacios disponibles para que los productores almacenen números.

  ii. non_emptylst: Esta lista almacena los semáforos de tipo Semaphore que representan la disponibilidad de elementos en los almacenes. Cada productor tiene su propio semáforo en esta lista. El número de semáforos en non_emptylst es igual al número de productores (NPROD). Cada semáforo se inicializa con un valor de 0, lo que indica que inicialmente no hay elementos disponibles para sacar en cada almacén.

  iii. mutexlst: Esta lista almacena los mutexes de tipo Lock que se utilizan para lograr exclusión mutua al acceder a los almacenes. Cada productor tiene su propio mutex en esta lista. El número de mutexes en mutexlst es igual al número de productores (NPROD). Cada mutex se utiliza para asegurar que solo un productor acceda a un almacén a la vez, garantizando la consistencia de los datos compartidos y la exclusión mutua.

- OPCIONAL: implmentación añadiendo un búffer de tamaño fijo de forma que los productores ponen valores en el búffer. Las principales diferencias con la anterior implementación son:

  i. emptylst: Esta lista almacena los semáforos de tipo BoundedSemaphore que representan la disponibilidad de espacios vacíos en los buffers de almacenamiento. Cada productor tiene su propio semáforo en esta lista. El número de semáforos en emptylst es igual al número de productores (NPROD). Cada semáforo se inicializa con un valor igual a la capacidad de los buffers (K), lo que indica que inicialmente hay espacios disponibles para que los productores almacenen números.

  ii. En la función add_data hay que esperar a que el valor del índice del respectivo proceso sea menor que K, porque sino accederá a una posición del almacén que no existe.
