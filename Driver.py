from ParkingGraph import ParkingGraph
import networkx as nx
from ParkingSpotState import ParkingSpotState
import numpy as np

class Driver:

    def __init__(self, G, position, goal, drivingSpeed):
        self.G = G
        self.position = position
        self.goal = goal
        self.drivingSpeed = drivingSpeed
        self.kb = {node : ParkingSpotState.UNKNOWN for node in self.G.nodes}

    def move(self, new_position):
        # move to new position if there exists an edge to it, and if the node is not occupied by a car 
        if new_position in self.getNeighbors() and self.kb[new_position] == ParkingSpotState.EMPTY:
            distance = np.sqrt((self.position[0] - new_position[0])**2 + (self.position[1] - new_position[1])**2)
            self.position = new_position
            return distance / self.drivingSpeed
        else: 
            return np.inf
        # the returns are for feedback to the strategy (error handling)

    def getGraph(self):
        return self.G
        
    def updateInformation(self):
        # TODO: change to update for each CURRENTLY VISIBLE node (now it's for every node)
        for node in self.G.nodes:
            if self.kb[node] == ParkingSpotState.UNKOWN:
                self.kb[node] = self.G.nodes[node]['state']
        pass

    def getInformation(self):
        return self.kb
    
    def getNeighbors(self):
        neighbors = [node for node in self.G.nodes if self.G.has_edge(self.position, node)]
        return neighbors
    
    def goalReached(self):
        return self.position == self.goal