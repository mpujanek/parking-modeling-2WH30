from Abstract_Strategy import Abstract_Strategy
from Abstract_Vis import Abstract_Vis
from ParkingSpotState import ParkingSpotState
from math import inf

class BackTrack_Strategy(Abstract_Strategy):

    def __init__(self, Visibility : Abstract_Vis):
        super().__init__(Visibility)
        self.isBacktracking = False

    
    def getNextStep(self) -> int:
        
        if not self.isValid(self.pos + 1):
            self.isBacktracking = True

        if not self.isBacktracking:
            self.pos += 1

        else:
            if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
                self.isFinished = True
                return self.pos
            self.pos -= 1
            
        return self.pos

    def resetStrat(self):
        super().resetStrat()
        self.isBacktracking = False