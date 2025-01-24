from Abstract_Strategy import Abstract_Strategy
from Abstract_Vis import Abstract_Vis
from ParkingSpotState import ParkingSpotState
from math import inf

class n_of_x_Strategy(Abstract_Strategy):

    def __init__(self, Visibility : Abstract_Vis, threshold : float, minTravel : int):
        super().__init__(Visibility)
        self.threshold = threshold
        self.n = minTravel
        self.isBackTrack = False
        self.isParking = False

    def getNextStep(self):
        vis = self.Visibility.getVisibility(self.pos)

        if self.isBackTrack:
            if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
                self.isFinished = True
                return self.pos
            self.pos -= 1
            return self.pos
        

        #Travel a minimum of N spots.
        if self.pos < self.n:
            self.pos += 1
            return self.pos
        
        #Busyness threshold has been passed, park ASAP.
        if self.isParking:
            if self.parkingMatrix[self.pos] == ParkingSpotState.EMPTY:
                self.isFinished = True
                return self.pos
            if self.isValid(self.pos + 1):
                self.pos += 1
            else:
                self.isBackTrack = True
            return self.pos

        #If it isn't too busy, continue on.
        if vis[0 : self.pos].count(ParkingSpotState.FULL) / (self.pos) < self.threshold:
            if self.isValid(self.pos + 1):
                self.pos += 1
                return self.pos
            self.isBackTrack = True
            return self.pos
        
        #Only comes here if it's passed initial N spots and it is too busy.
        self.isParking = True
        return self.pos

    def resetStrat(self):
        super().resetStrat()
        self.isBackTrack = False
        self.isParking = False

    def getName(self):
        return "Density threshold"