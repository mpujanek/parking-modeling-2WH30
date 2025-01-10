from Abstract_Vis import Abstract_Vis
from ParkingSpotState import ParkingSpotState

class SimpleVis(Abstract_Vis):

    def __init__(self, visionRange = 1):
        self.visionRange = visionRange

    def getVisibility(self, position : int):
        for i in range(self.visionRange + 1):
            view = position + i
            if (view >= len(self.parkingMatrix)):
                break
            self.visMatrix[view] = self.parkingMatrix[view]
        return self.visMatrix
    
    def resetVis(self):
        self.visMatrix = [ParkingSpotState.UNKNOWN] * len(self.visMatrix)
