from abc import ABC, abstractmethod
from Abstract_Vis import Abstract_Vis

class Abstract_Strategy(ABC):

    def __init__(self, Visibility : Abstract_Vis):
        self.Visibility = Visibility
        self.isFinished = False
        self.pos = 0

    #getNextStep returns the next position of the strategy.
    #returns True if the strategy is finished.
    @abstractmethod
    def getNextStep(self) -> int:
        vis = self.Visibility.getVisibility(self.pos)
        pass

    @abstractmethod
    def resetStrat(self):
        self.Visibility.resetVis()
        self.isFinished = False
        self.pos = 0
        pass

    def setMatrix(self, parkingMatrix : list):
        self.parkingMatrix = parkingMatrix
        self.Visibility.setMatrix(parkingMatrix)

    def _isFinished(self) -> bool:
        return self.isFinished

    def isValid(self, nextPos : int) -> bool:
        if (nextPos < 0 or nextPos >= len(self.parkingMatrix)):
            return False
        return True
    
    def getVisibility(self) -> list:
        return self.Visibility.getVisibility(self.pos)