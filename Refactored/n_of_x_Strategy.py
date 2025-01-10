from Abstract_Strategy import Abstract_Strategy
from Abstract_Vis import Abstract_Vis
from ParkingSpotState import ParkingSpotState
from math import inf

class n_of_x_Strategy(Abstract_Strategy):

    def __init__(self, Visibility : Abstract_Vis, threshold : float, minTravel : int):
        super().__init__(Visibility)
        self.threshold = threshold
        self.minTravel = minTravel
        self.isBackTrack = False
        self.isParking = False

    def getNextStep(self):
        vis = self.Visibility.getVisibility(self.pos)
        nextPos = self.pos

        if self.isBackTrack:
            if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
                self.isFinished = True
                return self.pos
            
            nextPos = self.pos - 1
            if self.isValid(nextPos):
                self.pos = nextPos
                return nextPos
            self.isFinished = True
            return -inf
                
        #Assume minTravel is smaller than number of parking spots.
        if self.pos < self.minTravel - 1:
            nextPos += 1
            self.pos = nextPos
            return nextPos
        
        #Edge case for if no cars are in the first x spots.
        if vis.count(ParkingSpotState.FULL) == 0:
            nextPos += 1
            if self.isValid(nextPos):
                self.pos = nextPos
                return nextPos
            self.isFinished = True
            return self.pos
        
        #Not busy, always continue if possible.
        if vis.count(ParkingSpotState.FULL) / self.pos < self.threshold and not self.isParking:
            nextPos += 1
            if self.isValid(nextPos):
                self.pos = nextPos
                return nextPos
            self.isBackTrack = True
            return self.pos

        #Busy, park asap.
        self.isParking = True

        if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
            self.isFinished = True
            return self.pos
        
        nextPos += 1
        if self.isValid(nextPos):
            self.pos = nextPos
            return nextPos

        self.isBackTrack = True
        return self.pos
            

    def resetStrat(self):
        super().resetStrat()
        self.isBackTrack = False
        self.isFinished = False