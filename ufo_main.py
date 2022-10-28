from py4j.java_gateway import JavaGateway
from ufo_autopilot import flight_distance_mult
from ufo_autopilot import fly_to
from ufo_routing import fac
from ufo_routing import find_shortest_route
from operator import itemgetter
from ufo_autopilot import distance_from_zero
from ufo_protocol import plot_protocol

# Initialisierung des Gateways zur Java-Ufo-Simulation
gateway = JavaGateway()

# In der folgenden Zeile definieren wir eine Referenz auf die Simulation.
sim = gateway.entry_point
sim.reset()

# Oeffnen einer View, die immer on Top angezeigt wird.
# Die Skalierung ist 10 m pro Pixel.
sim.openViewWindow(True, 10)

# Startpunkt p1 & Konsoleingabe der Flughoehe z 
p1 = (0.0 ,0.0)
z = float(input("z > 0 eingeben: "))

# Zielliste(n): 
destinations = [(55.0, 20.0), (-115.0, 95.0), (-116.5, 95.0), (-10.0, -40.0)]
## destinations = [(125.0, 20.0), (125.0, 19.9), (0.5, 0.5), (10.0, 20.0)]
## destinations = [(15.0, 15.0), (-15.0, 20.0), (-16.5, 5.0), (10.0, -4.0),(15.0, 15.0), (-15.0, 20.0), (-16.5, 5.0), (10.0, -4.0)]
## destinations = [(5.0,0.0),(5.0,0.0)]
## destinations = [(0.0,0.0)]
## destinations = []
# Hinzufügen der Ziele in die Simulation:
for i in destinations:
    x = i[0]
    y = i[1]
    sim.addDestination(x,y)

# Simulationsgeschwindigkeit setzen
sim.setSpeedup(10)

# Ausgabe der Anzahl der möglichen Strecken: 
n = len(destinations)
print(f"The number of possible routes is {fac(n)}")

# Meldung auf die Konsole ausgeben und auf Eingabe warten
input("Press return to start...")

# Abruf der kürzesten Strecke:
destinations = find_shortest_route(destinations)

# 10a Routingstrategie aufsteigend nach x-Koordinate:
#destinations = destinations.sort(key=itemgetter(0))

# 10b Routingstrategie aufsteigend nach Entfernung:
# destinations = destinations.sort(key=distance_from_zero)

# Hier Konsolausgabe der zu fliegenden Distanz ergaenzen
print(f"The Ufo has to fly a total distance of {flight_distance_mult(destinations,z)}")

# Fliege das Ufo zum Ziel
for i in destinations:
    x = i[0]
    y = i[1]
    p2 = (x,y)
    fly_to(sim, p2, z)
if len(destinations) != 0:
    fly_to(sim,p1,z)

# Hier Konsolausgabe der tatsaechlich geflogenen Distanz ergaenzen
print(f"The Ufo flew a distance of {sim.getDist()}")
print(plot_protocol(destinations))
