from abc import ABC, abstractmethod
from ParkingSpotState import ParkingSpotState

class Abstract_ProbDist(ABC):


    @abstractmethod
    def getParkingLotState(self, pos : int) -> ParkingSpotState:
        pass
