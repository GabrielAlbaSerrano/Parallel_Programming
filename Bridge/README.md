# Bridge
I have developed a Python monitor that simulates a bridge in which pedestrians and cars cannot share the bridge at the same time. Furthermore, due to the width of the bridge, cars traveling North and cars traveling South cannot share the bridge simultaneously either. Mutual exclusion is necessary based on the problem's conditions, and there must be an absence of starvation and deadlocks among the different processes (pedestrians, Northbound cars, Southbound cars) of the program.

To implement this monitor, I have created a Python class with its corresponding condition functions that allow or prohibit passage onto the bridge for each type of process. The entry and exit operations on the bridge are regulated by a Lock semaphore. To achieve mutual exclusion, absence of starvation, and absence of deadlocks, I have defined a 'value' named "turn" associated with the Python monitor class. The "turn" satisfies the following conditions:
- When "turn" = 0, pedestrians cannot pass, meaning cars can pass in both directions.
- When "turn" = 1, Northbound cars cannot pass, meaning pedestrians or Southbound cars can pass.
- When "turn" = 2, Southbound cars cannot pass, meaning pedestrians or Northbound cars can pass.

Once a process type (pedestrians, Northbound cars, or Southbound cars) exits the bridge, no more processes of that type can enter the bridge; in other words, "turn" takes a value that prevents it. When all processes of a particular type have exited the bridge, ALL condition signals of that process type with the highest number of waiting processes to enter are activated. To prevent starvation, if there is a single type of process that wants to enter and the "turn" value prevents it, the condition function of that process type is activated in this case.

The program's code can be found in the file 'Practica2_GabrielAlbaSerrano.py', and the file 'Practica2_GabrielAlbaSerrano_solucion_papel.pdf' contains the pseudocode of the program, its explanation, and also the demonstrations of the invariant being upheld after each operation function, along with proofs of mutual exclusion, absence of deadlock, and absence of starvation.

-----------------------------------

# Puente
He desarrollado un monitor en Python que simula un puente en el cual los peatones y los coches no pueden compartir el puente, y además por la anchura del puente los coches de dirección Norte y los coches de dirección Sur NO pueden tampoco compartir el puente. Es necesario que haya exclusión mutua según las condiciones del problema y haya ausencia de inanición (starvation) y de punto muerto (deadlock) entre los diferentes procesos (peatones, coches Norte, coches Sur) del programa.

Para implementar dicho monitor he creado una clase en Python, con sus respectivas funciones condición que permiten o prohíben el paso al puente a cada tipo de proceso, y sus funciones operación de entrar y salir al puente, todo ello está regulado por un semáforo Lock. Para conseguir la exclusión mutua y la ausencia de inanición y punto muerto he definido un 'value' turno asociado a la clase monitor en Python que cumple que:
turno = 0 --> NO pueden pasar peatones, es decir, pueden pasar coches en ambas direcciones
turno = 1 --> NO pueden pasar coches Norte, es decir, pueden pasar peatones o coches Sur
turno = 2 --> NO pueden pasar coches Sur es decir, pueden pasar peatones o coches Norte

Cuando un tipo de proceso (peatones, coches Norte o coches Sur) sale del puente, entonces no pueden pasar más procesos de ese tipo al puente, es decir, turno tiene el valor que lo prohíbe. Cuando hayan salido todos los procesos de un tipo del puente, se activan TODAS las señales de condición del tipo de proceso que tiene más cantidad de procesos esperando para entrar. Para evitar la inanición, si hay un único tipo de proceso que quiera entrar y el 'value' turno lo impide, entonces en este caso la función condición de ese tipo de proceso se activa.
El código del programa es el archivo 'Practica2_GabrielAlbaSerrano.py' y el archivo 'Practica2_GabrielAlbaSerrano_solucion_papel.pdf' contiene el pseudocódigo del programa y su explicaión, y además, la demostración de que se cumple el invariante después de cada función operación y las demostraciones de exclusión mutua, ausencia de deadlock y ausencia de inanición.
