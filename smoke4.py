import math
from py4j.java_gateway import JavaGateway
from ufo_autopilot import distance
from ufo_autopilot import distance_from_zero
from ufo_autopilot import angle
from ufo_autopilot import flight_distance
from ufo_autopilot import flight_distance_mult
from ufo_autopilot import fly_to
from ufo_autopilot import format_flight_data
from ufo_autopilot import takeoff
from ufo_autopilot import cruise
from ufo_autopilot import landing
from ufo_routing import fac
from ufo_routing import find_shortest_route
from ufo_protocol import add_to_protocol
from ufo_protocol import plot_protocol
from ufo_protocol import protocol_x
from ufo_protocol import protocol_y

# Globale Variablen
test = 0
ergebnis = ""

# Funktion zur Testauswertung
def assertEqual(ist, soll, delta=0):
    global test
    global ergebnis
    test = test + 1
    if abs(ist - soll) > delta:
        ergebnis = ergebnis + "\nFehler in Test " + str(test) + ": Ist-Wert " + str(ist) + ", Soll-Wert " + str(soll)

# Initialisierung der Ufo-Simulation
gateway = JavaGateway()
sim = gateway.entry_point
sim.setSpeedup(10)

# Tests
assertEqual(distance((1.0, 1.0), (0.0, 2.0)), math.sqrt(2.0), 1e-3) #1
assertEqual(distance_from_zero((1.0, -2.0)), math.sqrt(5.0), 1e-3) #2
assertEqual(angle((1.0, 1.0), (2.0, 0.0)), 315.0, 1e-3) #3
assertEqual(flight_distance((1.0, 1.0), (2.0, 1.0), 10.0), 21.0, 1e-3) #4
assertEqual(flight_distance_mult([(20.0, 20.0), (20.0, 0.0)], 10.0), math.sqrt(800.0)+100.0, 1e-3) #5

sim.reset()
format_flight_data(sim)

sim.reset()
fly_to(sim, (20.0, 20.0), 10.0)
assertEqual(sim.getX(), 20.0, 1.0) #6
assertEqual(sim.getY(), 20.0, 1.0) #7
assertEqual(sim.getZ(), 0.0, 0.1) #8

sim.reset()
fly_to(sim, (20.0, 0.0), 10.0)
assertEqual(sim.getX(), 20.0, 1.0) #9
assertEqual(sim.getY(), 0.0, 1.0) #10
assertEqual(sim.getZ(), 0.0, 0.1) #11

sim.reset()
takeoff(sim, 10.0)
cruise(sim, (20.0, 20.0))
landing(sim)

assertEqual(fac(5,3), 60) #12
assertEqual(fac(4), 24) #13

destinations = [(55.0, 20.0), (-116.5, 95.0), (-10.0, -40.0), (-115.0, 95.0)]
assertEqual(flight_distance_mult(find_shortest_route(destinations), 10.0), 559.0149, 1e-3) #14
assertEqual(flight_distance_mult(find_shortest_route([]), 10.0), 0.0, 1e-3) #15

l = len(protocol_x)
add_to_protocol((1.1, 2.2))
assertEqual(protocol_x[-1], 1.1, 1e-3) #16
assertEqual(protocol_y[-1], 2.2, 1e-3) #17
assertEqual(len(protocol_x), l+1) #18
assertEqual(len(protocol_y), l+1) #19

# Ausgabe des Testergebnisses
print()
print("Es wurden", test, "Tests ausgefuehrt. ", end="")
if ergebnis == "":
    print("OK.")
else:
    print(ergebnis)
