from Abstract_ProbDist import Abstract_ProbDist
from ParkingSpotState import ParkingSpotState
from random import random


class Linear_PropDist(Abstract_ProbDist):

    def __init__(self, nParkingSpots : int, p_start = 1.0, p_end = 0.3):
        super().__init__()
        self.nParkingSpots = nParkingSpots
        self.p_start = p_start
        self.p_end = p_end

    def getParkingLotState(self, pos):
        threshold = (pos / self.nParkingSpots) * self.p_start + (1 - pos/self.nParkingSpots) * self.p_end
        return ParkingSpotState.FULL if random() < threshold else ParkingSpotState.EMPTY