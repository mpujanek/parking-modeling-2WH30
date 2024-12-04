import numpy as np
from ParkingSpotState import ParkingSpotState
from pprint import pprint
import random

class ParkingMatrix:

    def __init__(self, nSpotsInRow, nBlocks, doubleRows, visionRange):
        factor = 3 if doubleRows else 2
        self.nSpotsInRow = nSpotsInRow
        self.knownSpots = [ParkingSpotState.UNKNOWN] * nSpotsInRow
        self.position = 0
        self.visionRange = visionRange
        #self.matrix = [[ParkingSpotState.ROAD if (x==0 or x==nspotsInRow+1 or y %factor == 0) else ParkingSpotState.EMPTY for x in range(nspotsInRow + 2)] for y in range(factor*nBlocks+1)]
        self.matrix = [ParkingSpotState.EMPTY for x in range(nSpotsInRow)]

    def getMatrix(self):
        return self.matrix
    
    
    def visibility(self, position : int) -> list:
        for i in range(self.visionRange + 1):
            self.knownSpots[position + i] = self.getMatrix[position + i]

    # run the strategy once and return the time it took to find a spot
    def run(self, timeLimit):
        time = 0
        while(not self.driver.goalReached()):
            next_pos = self.determineNextPosition()
            time += self.driver.move(next_pos)
            if time > timeLimit:
                return np.inf
            
        return time
    
    # run the strategy on the same graph 
    def test(self, timeLimit, iters=10):
        data = pd.DataFrame({'time': []})
        for i in range(iters):
            time = self.run(timeLimit)
            data.loc[i,'time'] = time
        print(data)

    def populate_bernoulli(self, p):
        for i in range(self.nspotsInRow):
            self.matrix[i] = ParkingSpotState.FULL if random.random() < p else ParkingSpotState.EMPTY

    def visualize(self):
        pprint(self.matrix)

ParkingMatrix(6,1, False)