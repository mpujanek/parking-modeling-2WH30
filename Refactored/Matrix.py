from ParkingSpotState import ParkingSpotState
from Abstract_ProbDist import Abstract_ProbDist

class PMatrix:

    def __init__(self, nSpotsInRow : int, distribution : Abstract_ProbDist):
        self.distribution = distribution
        self.nSpotsInRow = nSpotsInRow
        self.matrix = []
        self.regenarateMatrix()

    
    def getMatrix(self):
        return self.matrix
    
    def setDist(self, distribution: Abstract_ProbDist):
        self.distribution = distribution
    
    def regenarateMatrix(self):
        matrix = []
        #Regenerate until there is a free spot.
        while (matrix.count(ParkingSpotState.FULL) == len(matrix)):    
            matrix = []
            for i in range(self.nSpotsInRow):
                matrix.append(self.distribution.getParkingLotState(i))
        
        self.matrix = matrix
        return self.getMatrix()