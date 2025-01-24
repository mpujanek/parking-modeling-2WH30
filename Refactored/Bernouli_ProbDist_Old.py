from Abstract_ProbDist import Abstract_ProbDist
from ParkingSpotState import ParkingSpotState
from random import random

class Bernouli_Probdist_Old(Abstract_ProbDist):

    def __init__(self, nrOfParkingSpots : int, busyness):
        self.nrOfParkingSpots = nrOfParkingSpots
        self.b = busyness / 100

    def getParkingLotState(self, pos):
        p = self.b
        return ParkingSpotState.FULL if random() < p else ParkingSpotState.EMPTY
    