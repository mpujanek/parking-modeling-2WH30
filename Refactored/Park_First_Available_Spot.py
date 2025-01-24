from Abstract_Strategy import Abstract_Strategy
from Abstract_Vis import Abstract_Vis
from ParkingSpotState import ParkingSpotState

class ParkFirstAvailableSpot(Abstract_Strategy):

    def __init__(self, Visibility : Abstract_Vis):
        super().__init__(Visibility)


    def getNextStep(self):
        if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
            self.isFinished = True
        else: self.pos += 1
        return self.pos
    
    def resetStrat(self):
        return super().resetStrat()
    
    def getName(self):
        return "First available spot"