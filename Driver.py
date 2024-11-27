import ParkingGraph
import networkx as nx
import ParkingSpotState

class Driver:

    def __init__(self, G: ParkingGraph, position):
        self.G = G
        self.position = position
        self.kb = {node : ParkingSpotState.UNKNOWN for node in self.G.nodes}

    def move(self, new_position):
        # move to new position if there exists an edge to it, and if the node is not occupied by a car 
        if self.G.has_edge(self.position, new_position) and not self.G.nodes[new_position].get('occupied'):
            self.position = new_position
            return True
        else: 
            return False
        # the returns are for feedback to the strategy (error handling)
        
    def updateInformation(self):
    # for each currently visible node
        # if node state is unknown in kb
            # self.kb[node] = self.G.nodes[node].get('state')
        pass

    def getInformation(self):
        return self.kb