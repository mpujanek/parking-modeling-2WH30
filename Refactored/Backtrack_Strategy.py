from Abstract_Strategy import Abstract_Strategy
from Abstract_Vis import Abstract_Vis
from ParkingSpotState import ParkingSpotState
from math import inf

class BackTrack_Strategy(Abstract_Strategy):

    def __init__(self, Visibility : Abstract_Vis):
        super().__init__(Visibility)
        self.isBacktracking = False

    
    def getNextStep(self) -> int:
        
        if not self.isBacktracking:
            nextPos = self.pos + 1
            # Reached end of the row.
            if not self.isValid(nextPos):
                nextPos = nextPos - 1
                if self.parkingMatrix[nextPos] == ParkingSpotState.EMPTY:
                    self.isFinished = True
                else:
                    self.isBacktracking = True

        if self.isBacktracking:
            nextPos = self.pos - 1
            if not self.isValid(nextPos):
                #Strategy is finished.
                nextPos = -inf
                self.isFinished = True
            if self.parkingMatrix[nextPos] == ParkingSpotState.EMPTY:
                self.isFinished = True

        self.pos = nextPos
        return nextPos

    def resetStrat(self):
        super().resetStrat()
        self.isBacktracking = False