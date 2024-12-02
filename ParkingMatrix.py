import numpy as np
from ParkingSpotState import ParkingSpotState
from pprint import pprint

class ParkingMatrix:

    def __init__(self, nspotsInRow, nBlocks, doubleRows):
        factor = 3 if doubleRows else 2
        self.matrix = [[ParkingSpotState.ROAD if (x==0 or x==nspotsInRow+1 or y %factor == 0) else ParkingSpotState.EMPTY for x in range(nspotsInRow + 2)] for y in range(factor*nBlocks+1)]
        pprint(self.matrix)


    def getMatrix(self):
        return self.matrix

ParkingMatrix(6,2, True)