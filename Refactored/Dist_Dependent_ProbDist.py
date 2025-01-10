from Abstract_ProbDist import Abstract_ProbDist
from random import random
from ParkingSpotState import ParkingSpotState
from math import exp


class distDependentProb(Abstract_ProbDist):

    def __init__(self, nParkingSpots : int, busyness : int):
        self.nParkingSpots = nParkingSpots
        self.b = busyness

    
    def getParkingLotState(self, pos):
        super().getParkingLotState(pos)
        rand = random()
        if rand >= exp(-(self.nParkingSpots - pos) / (1 + self.b)):
            return ParkingSpotState.EMPTY
        return ParkingSpotState.FULL