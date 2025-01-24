from Abstract_Strategy import Abstract_Strategy
from Abstract_Vis import Abstract_Vis
from ParkingSpotState import ParkingSpotState

class Park_After_N_Strategy(Abstract_Strategy):

    def __init__(self, Visibility : Abstract_Vis, parkAfterN : int):
        self.n = parkAfterN
        self.isBacktrack = False
        super().__init__(Visibility)


    def getNextStep(self):

        if self.isBacktrack:
            if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
                self.isFinished = True
                return self.pos
            self.pos -= 1
            return self.pos
        
        if self.pos < self.n - 1:
            self.pos += 1
            return self.pos
        
        if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
            self.isFinished = True
            return self.pos
        
        if self.isValid(self.pos + 1):
            self.pos += 1
            return self.pos
        
        self.isBacktrack = True
        return self.pos


    def resetStrat(self):
        super().resetStrat()
        self.isBacktrack = False

    def getName(self):
        return "Park after N spots"