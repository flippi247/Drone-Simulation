import math
from ufo_protocol import add_to_protocol

def distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    dist = math.sqrt((abs(x1-x2)**2+abs(y1-y2)**2))
    return dist

def angle(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    kathete1 = 0
    kathete2 = 0
    phi = float(0)
    if y2 == y1 and x2 == x1:
        ergebnis = False
    elif y2 >= y1 and x2 > x1:
        kathete1 = abs(x2 - x1)
        kathete2 = abs(y2 - y1)
        phi = math.atan(kathete2/kathete1)
        ergebnis = phi * 180 / math.pi
    elif y2 > y1 and x2 == x1:
        phi = float(90)
        ergebnis = phi
    elif y2 > y1  and x2 < x1:
        kathete1 = abs(x1 - x2)
        kathete2 = abs(y2 - y1)
        phi = math.atan(kathete2/kathete1)
        ergebnis = 180 - phi * 180 / math.pi
    elif  y2 == y1  and x2 < x1:
        phi = float(180)
        ergebnis = phi    
    elif  y2 < y1  and x2 < x1:
        kathete1 = abs(x1 - x2)
        kathete2 = abs(y1 - y2)
        phi = math.atan(kathete2 / kathete1)
        ergebnis = 180 + phi * 180 / math.pi
    elif  y2 < y1  and x2 == x1:
        phi = float(270)
        ergebnis = phi
    elif y2 < y1  and x2 > x1:
        kathete1 = abs(x2 - x1)
        kathete2 = abs(y1 - y2)
        phi = math.atan(kathete2 / kathete1)
        ergebnis = 360 - phi * 180 / math.pi
    return round(ergebnis,2)

def flight_distance(p1, p2 ,z):
    return 2 * z + distance(p1,p2)

def flight_distance_mult(destinations, z):
    p1 = (0.0, 0.0)
    p2 = (0.0, 0.0)
    dist = 0.0
    if len(destinations) == 1 and destinations[0] == (0.0,0.0):
        dist = 0.0
    elif len(destinations) >=1:
        dist += 2 * z + distance(p1, destinations[len(destinations)-1])
        for i in destinations:
            x2 = i[0]
            y2 = i[1]
            p2 = (x2,y2)
            # if p1 != p2:
            dist += (distance(p1,p2) + 2 * z)
            # else:
            #    dist += 0
            p1 = p2
    else:
        dist = 0.0
    return dist 

def format_flight_data(sim):
    dt = sim.getTime()
    dx = sim.getX()
    dy = sim.getY()
    dz = sim.getZ()
    return ("{0:>5.1f}{1:<6}{2:>6.1f}{3:>6.1f}{4:>6.1f}{5:>1}".format(dt, " s:  [", dx, dy, dz, "]"))
        
def fly_to(sim, p, z):
    fro_x = sim.getX()
    fro_y = sim.getY()
    fro_p = (fro_x, fro_y)
    if p != fro_p:
        takeoff(sim, z)
        cruise(sim, p)
        landing(sim)

def takeoff(sim, z):
    # Das Ufo fliegt senkrecht nach oben mit 10 km/h.
    print(str(format_flight_data(sim)) + "takeoff with 10 km/h to alt 10 m...")
    sim.setI(90)
    sim.requestDeltaV(10)

    # Rechtzeitig vor dem Erreichen der Zielhoehe, bremst das Ufo auf 1 km/h.
    while sim.getZ() < z - 2:
        pass
    print(format_flight_data(sim) + "...slow down to 1 km/h... ")
    sim.requestDeltaV(-9)
    
    # Wenn das Ufo ganz nahe dran ist, stoppt es und richtet sich horizontal aus.
    while sim.getZ() < z - 0.05:
        pass
    print(str(format_flight_data(sim)) + "...stop and turn horizontal")
    sim.requestDeltaV(-1)
    sim.setI(0)

def cruise(sim, p):
    # Das Ufo ist in der aktuellen Position gestartet.
    fro_x = sim.getX()
    fro_y = sim.getY()
    fro_p = (fro_x, fro_y)
    add_to_protocol(fro_p)

    # Weiter geht es in Richtung Ziel. Die zu fliegende Distanz ist dist.
    sim.setD(int(angle(fro_p, p)))
    dist = sim.getDist() + distance(fro_p, p)

    
    # Das Ufo beschleunigt auf 15 km/h.
    sim.requestDeltaV(15)
    
    # Wenn der Abstand zum Ziel 4m ist, bremst das Ufo auf 1 km/h.
    while dist - sim.getDist() > 4:
        add_to_protocol(fro_p)
        pass
    sim.requestDeltaV(-14)

    # Kurz vor dem Ziel richten wir das Ufo genau aus.
    fro_x = sim.getX()
    fro_y = sim.getY()
    fro_p = (fro_x,fro_y)
    add_to_protocol(fro_p)
    sim.setD(int(angle(fro_p, p)))
    dist = sim.getDist() + distance(fro_p, p)




    # Wenn der Abstand zum Ziel 0.05m ist, stoppt das Ufo.
    while dist - sim.getDist() > 0.05:
        pass
    sim.requestDeltaV(-1)
# Das Ufo fliegt senkrecht nach unten mit 10 km/h.
def landing(sim):
    print(format_flight_data(sim) + "landing with 10 km/h")
    sim.setI(-90)
    sim.requestDeltaV(10)
    
    # Wenn die Hoehe 3m erreicht, bremst das Ufo auf 1 km/h.
    while sim.getZ() > 3:
        pass
    print(format_flight_data(sim) + "...slow down to 1 km/h...")
    sim.requestDeltaV(-9)
    
    # Das Ufo ist gelandet, wenn die Hoehe kleiner gleich 0 ist.
    while sim.getZ() > 0:
        pass
    print(format_flight_data(sim) + "...happily landed")

def distance_from_zero(p):
    p1 = (0.0, 0.0)
    return distance(p1,p)

