# Bridge
I have developed a Python monitor that simulates a bridge in which pedestrians and cars cannot share the bridge at the same time. Furthermore, due to the width of the bridge, cars traveling North and cars traveling South cannot share the bridge simultaneously either. Mutual exclusion is necessary based on the problem's conditions, and there must be an absence of starvation and deadlocks among the different processes (pedestrians, Northbound cars, Southbound cars) of the program.

To implement this monitor, I have created a Python class with its corresponding condition functions that allow or prohibit passage onto the bridge for each type of process. The entry and exit operations on the bridge are regulated by a Lock semaphore. To achieve mutual exclusion, absence of starvation, and absence of deadlocks, I have defined a 'value' named "turn" associated with the Python monitor class. The "turn" satisfies the following conditions:
- When "turn" = 0, pedestrians cannot pass, meaning cars can pass in both directions.
- When "turn" = 1, Northbound cars cannot pass, meaning pedestrians or Southbound cars can pass.
- When "turn" = 2, Southbound cars cannot pass, meaning pedestrians or Northbound cars can pass.

Once a process type (pedestrians, Northbound cars, or Southbound cars) exits the bridge, no more processes of that type can enter the bridge; in other words, "turn" takes a value that prevents it. When all processes of a particular type have exited the bridge, ALL condition signals of that process type with the highest number of waiting processes to enter are activated. To prevent starvation, if there is a single type of process that wants to enter and the "turn" value prevents it, the condition function of that process type is activated in this case.

The program's code can be found in the file 'Practica2_GabrielAlbaSerrano.py', and the file 'Practica2_GabrielAlbaSerrano_solucion_papel.pdf' contains the pseudocode of the program, its explanation, and also the demonstrations of the invariant being upheld after each operation function, along with proofs of mutual exclusion, absence of deadlock, and absence of starvation.
