from Abstract_ProbDist import Abstract_ProbDist
from ParkingSpotState import ParkingSpotState
from random import random


class Linear_PropDist(Abstract_ProbDist):

    def __init__(self, nParkingSpots : int, p_min = 1.0, p_max = 0.3):
        super().__init__()
        self.nParkingSpots = nParkingSpots
        self.p_min = p_min
        self.p_max = p_max

    def getParkingLotState(self, pos):
        threshold = self.p_min + pos / self.nParkingSpots * (self.p_max - self.p_min)
        return ParkingSpotState.FULL if random() < threshold else ParkingSpotState.EMPTY