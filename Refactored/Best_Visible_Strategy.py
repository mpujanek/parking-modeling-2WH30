from Abstract_Strategy import Abstract_Strategy
from ParkingSpotState import ParkingSpotState
from math import inf

class BestVisibleSpotStrategy(Abstract_Strategy):

    def __init__(self, Visibility):
        super().__init__(Visibility)
    
    def getNextStep(self):
        vis = self.Visibility.getVisibility(self.pos)

        #We must advance if we're in a full spot
        if self.parkingMatrix[self.pos] == ParkingSpotState.FULL:
            if self.isValid(self.pos + 1):
                self.pos += 1
                return self.pos
            else: 
                self.isFinished = True
                return self.pos
            
        #we are in an empty spot, look ahead if a better spot exists.
        for i in range(self.pos + 1, len(self.parkingMatrix)):
            if vis[i] == ParkingSpotState.EMPTY:
                self.pos += 1
                return self.pos

        self.isFinished = True
        return self.pos
    
    def resetStrat(self):
        super().resetStrat()