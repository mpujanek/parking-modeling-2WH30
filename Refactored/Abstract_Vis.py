from abc import ABC, abstractmethod
from ParkingSpotState import ParkingSpotState

class Abstract_Vis(ABC):

    def setMatrix(self, parkingMatrix : list):
        self.parkingMatrix = parkingMatrix
        self.visMatrix = [ParkingSpotState.UNKNOWN] * len(parkingMatrix)

    @abstractmethod
    def getVisibility(self, position : int) -> list:
        pass

    @abstractmethod
    def resetVis(self):
        pass