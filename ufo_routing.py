import math
import itertools
from ufo_autopilot import flight_distance_mult

def fac(m=1,n=1):
    if m == 1:
        return 1
    elif n > m:
        return 1
    elif m == n:
        return m
    else:
        return n * fac(m - 1, n + 1) * m


def find_shortest_route(destinations):
    routes = list(itertools.permutations(destinations))
    shortest_dist = flight_distance_mult(routes[0],0.1)
    shortest_path = routes[0]
    k=0
    for i in routes:
        if shortest_dist > flight_distance_mult(list(i),0.1):
            shortest_path = list(routes[k])
            shortest_dist = flight_distance_mult(list(i),0.1)
        k = k + 1  
    return list(reversed(shortest_path))