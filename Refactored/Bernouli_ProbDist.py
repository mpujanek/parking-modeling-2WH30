from Abstract_ProbDist import Abstract_ProbDist
from random import random
from ParkingSpotState import ParkingSpotState

class Bernouli_ProbDist(Abstract_ProbDist):

    def __init__(self, p = 0.5):
        self.p = p

    def getParkingLotState(self, pos):
        super().getParkingLotState(pos)
        if random() <= self.p:
            return ParkingSpotState.FULL
        return ParkingSpotState.EMPTY