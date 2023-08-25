
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 20
NPED = 100
TIME_CARS_NORTH = 0.5  # a new car enters each 0.5s
TIME_CARS_SOUTH = 0.5  # a new car enters each 0.5s
TIME_PED = 1 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (2, 1) # normal 1s, 0.5s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.carnorth = Value('i', 0)
        self.carsouth = Value('i', 0)
        self.ped = Value('i', 0)
        self.carnorth_waiting = Value('i', 0)
        self.carsouth_waiting = Value('i', 0)
        self.ped_waiting = Value('i', 0)
        self.ok_carnorth = Condition(self.mutex)
        self.ok_carsouth = Condition(self.mutex)
        self.ok_ped = Condition(self.mutex)
        self.turn = Value('i', -1)
        #turn 0: no for pedestrians (== for car north and car south)
        #turn 1: no for cars north (== for pedestrians and car south)
        #turn 2: no for cars south (== for pedestrians and car north)

    #Las condiciones is_ok_X se cumplen cuando no hay procesos de distinto
    #tipo a X en el puente, y cuando el turno no prohibe entrar a X, o
    #no hay procesos de otros tipos esperando para entrar en el puente

    def is_ok_ped(self):
        return self.carnorth.value == 0 and self.carsouth.value == 0 \
            and (self.turn.value != 0 or (self.carnorth_waiting.value == 0 and self.carsouth_waiting.value == 0))
    
    def is_ok_carnorth(self):
        return self.ped.value == 0 and self.carsouth.value == 0 \
            and (self.turn.value != 1 or (self.ped_waiting.value == 0 and self.carsouth_waiting.value == 0))
    
    def is_ok_carsouth(self):
        return self.carnorth.value == 0 and self.ped.value == 0 \
            and (self.turn.value != 2 or (self.carnorth_waiting.value == 0 and self.ped_waiting.value == 0))

    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        if direction == NORTH:
            self.carnorth_waiting.value += 1
            self.ok_carnorth.wait_for(self.is_ok_carnorth)
            self.carnorth_waiting.value -= 1
            self.carnorth.value += 1
        if direction == SOUTH:
            self.carsouth_waiting.value += 1
            self.ok_carsouth.wait_for(self.is_ok_carsouth)
            self.carsouth_waiting.value -= 1
            self.carsouth.value += 1
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        if direction == NORTH:
            self.carnorth.value -=1
            #Cuando sale del puente un coche direccion norte, no pueden entrar
            #mas hasta que pasen los peatones o los coches direccion sur,
            #dependiendo de los que tengan mayor cantidad esperando para entrar.
            self.turn.value = 1
            if self.carnorth.value == 0:
                if self.ped_waiting.value >= self.carsouth_waiting.value:
                    self.ok_ped.notify_all()
                else:
                    self.ok_carsouth.notify_all()
        if direction == SOUTH:
            self.carsouth.value -=1
            #Cuando sale del puente un coche direccion sur, no pueden entrar
            #mas hasta que pasen los peatones o los coches direccion norte,
            #dependiendo de los que tengan mayor cantidad esperando para entrar
            self.turn.value = 2
            if self.carsouth.value == 0:
                if self.ped_waiting.value >= self.carnorth_waiting.value:
                    self.ok_ped.notify_all()
                else:
                    self.ok_carnorth.notify_all()
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.ped_waiting.value += 1
        self.ok_ped.wait_for(self.is_ok_ped)
        self.ped_waiting.value -= 1
        self.ped.value += 1
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.ped.value -= 1
        #Cuando sale del puente un peaton, no pueden entrar mas hasta 
        #que pasen los coches sur o norte, dependiendo de los que tengan 
        #mayor cantidad esperando para entrar.
        self.turn.value = 0
        if self.ped.value == 0:
            if self.carnorth_waiting.value >= self.carsouth_waiting.value:
                self.ok_carnorth.notify_all()
            else:
                self.ok_carsouth.notify_all()
        self.mutex.release()

    def __repr__(self) -> str:
        return f'< Monitor: p:{self.ped.value}, cn:{self.carnorth.value}, cs:{self.carsouth.value}, pw:{self.ped_waiting.value}, cnw:{self.carnorth_waiting.value}, csw:{self.carsouth_waiting.value}, turn:{self.turn.value} >'

def delay_car_north() -> None:
    time.sleep(random.uniform(*TIME_IN_BRIDGE_CARS))

def delay_car_south() -> None:
    time.sleep(random.uniform(*TIME_IN_BRIDGE_CARS))

def delay_pedestrian() -> None:
    time.sleep(random.uniform(*TIME_IN_BRIDGE_PEDESTRIAN))

def car(cid: int, direction: int, monitor: Monitor)  -> None:
    print(f"{monitor} -- Car {cid} heading {direction} wants to enter.")
    monitor.wants_enter_car(direction)
    print(f"{monitor} -- Car {cid} heading {direction} enters the bridge.")
    if direction==NORTH :
        delay_car_north()
    else:
        delay_car_south()
    print(f"{monitor} -- Car {cid} heading {direction} leaving the bridge.")
    monitor.leaves_car(direction)
    print(f"{monitor} -- Car {cid} heading {direction} out of the bridge.")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"{monitor} -- Pedestrian {pid} wants to enter.")
    monitor.wants_enter_pedestrian()
    print(f"{monitor} -- Pedestrian {pid} enters the bridge.")
    delay_pedestrian()
    print(f"{monitor} -- Pedestrian {pid} leaving the bridge.")
    monitor.leaves_pedestrian()
    print(f"{monitor} -- Pedestrian {pid} out of the bridge.")



def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(direction: int, time_cars, monitor: Monitor) -> None:
    cid = 0
    plst = []
    for _ in range(NCARS):
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/time_cars))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars_north = Process(target=gen_cars, args=(NORTH, TIME_CARS_NORTH, monitor))
    gcars_south = Process(target=gen_cars, args=(SOUTH, TIME_CARS_SOUTH, monitor))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars_north.start()
    gcars_south.start()
    gped.start()
    gcars_north.join()
    gcars_south.join()
    gped.join()


if __name__ == '__main__':
    main()
