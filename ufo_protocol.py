import matplotlib.pyplot as plt

protocol_x = []
protocol_y = []

def add_to_protocol(p):
    x,y = p
    protocol_x.append(x)
    protocol_y.append(y)
    

def plot_protocol(destinations):
    global protocol_x
    global protocol_y

    #Hinzufügen des Startwerts, da dieser nicht in der Zielliste enthalten ist.
    destinations_x = []
    destinations_y = []

    # # Abfgangen von leeren Listen & weiteren Problemchen
    # if (len(protocol_x) or len(protocol_y)) <= 1:
    #     pass

    # elif (len(protocol_x) or len(protocol_y)) >= 1:
    #     endpoint_x = protocol_x[len(protocol_x)-1]
    #     endpoint_y = protocol_y[len(protocol_y)-1]
    # # Hinzufügen des Endpunkts aus der geflogenen Route(als orangenen Punkt)
    #     destinations_x.append(endpoint_x)
    #     destinations_y.append(endpoint_y)

    # Splitten der Zieltupel in zwei Listen (X und Y)
    for i in destinations:
        destinations_x.append(i[0])
        destinations_y.append(i[1])

 
    # Erstellung des Diagramms
    plt.title("Ufo Flight Protocol")
    plt.scatter(destinations_x, destinations_y, color='orange')    
    plt.plot(protocol_x,protocol_y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
