import ParkingGraph
import networkx as nx
from ParkingSpotState import ParkingSpotState

class Vis:

    def __init__(self, G: ParkingGraph):
        self.G = G.getGraph()
        self.kb = {node : ParkingSpotState.UNKNOWN for node in self.G.nodes}

    
    def getNeighbors(self, position):
        neighbors = []
        for node in self.G.nodes:
            if self.G.has_edge(position, node):
                neighbors.append(node)
        #neighbors = [node for node in self.G.nodes if self.G.has_edge(position, node)]
        return neighbors

    # Will run a BFS to find the first visible cars.
    def getNewCars(self, position):
        queue = [position]
        while len(queue) > 0:
            newCars = []

            v = queue.pop
            #Getting neighbours seems to be an issue.
            for neighbour in self.getNeighbors(v):
                #Parking spot not yet explored
                print(neighbour)
                if self.kb[neighbour] == ParkingSpotState.UNKNOWN or self.kb[neighbour] == ParkingSpotState.EMPTY:
                    queue.append(neighbour)
                else:
                    #nx.get_node_attributes(self.G, "")
                    self.G.Graph.nodes[neighbour].get("occupied")
                    newCars.append(neighbour)
        return newCars