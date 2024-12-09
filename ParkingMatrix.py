import numpy as np
from ParkingSpotState import ParkingSpotState
from pprint import pprint
import random
import pandas as pd

class ParkingMatrix:

    def __init__(self, nSpotsInRow, visionRange, drivingSpeed):
        # factor = 3 if doubleRows else 2
        self.nSpotsInRow = nSpotsInRow
        self.knownSpots = [ParkingSpotState.UNKNOWN] * nSpotsInRow
        self.position = 0
        self.visionRange = visionRange
        self.drivingSpeed = drivingSpeed
        # extra stuff to use in strategy
        self.spotToParkIn = None
        self.moveDir = 1
        self.n = 0
        self.x = 0
        self.backTrack = False
        #self.matrix = [[ParkingSpotState.ROAD if (x==0 or x==nspotsInRow+1 or y %factor == 0) else ParkingSpotState.EMPTY for x in range(nspotsInRow + 2)] for y in range(factor*nBlocks+1)]
        self.matrix = [ParkingSpotState.EMPTY] * nSpotsInRow

    def getMatrix(self):
        return self.matrix
    
    
    def visibility(self, position):
        for i in range(self.visionRange + 1):
            self.knownSpots[position + i] = self.getMatrix()[position + i]

    # returns index of the visible spot that is closest to the STORE ENTRANCE, None if no such spot exists
    def closestVisibleSpot(self):
        index = None
        for i in range(len(self.knownSpots)):
            if self.knownSpots[i] == ParkingSpotState.EMPTY:
                index = i
        return index

    # moves position to next position and returns the time it took to get there
    # assumes next position is a valid index in the parking lot
    def move(self, next_position):
        distance = float(abs(self.position - next_position))
        self.position = next_position
        return distance / float(self.drivingSpeed)
    
    # returns next step (position) towards desired spot
    # assumes desired spot is different than current
    def stepTowards(self, next_position):
        if self.position - next_position < 0:
            return self.position + 1
        elif self.position - next_position > 0:
            return self.position - 1
        else: 
            return self.position

    def backtrackStrategy(self):
        if self.position == len(self.matrix) - 1:
            self.backTrack = True

        if not self.backTrack:
            return self.position + 1
        
        else:
            if self.matrix[self.position] == ParkingSpotState.EMPTY:
                self.spotToParkIn = self.position
                return self.position
            return self.position - 1

            


        


    # assumes there is a parking spot available and no changes in parked cars
    def bestVisibleSpot(self):
        if self.position == 0:
            # update visibility
            self.visibility(self.position)

            # determine furthest empty spot visible from entrance
            self.spotToParkIn = self.closestVisibleSpot()

            # if no empty spot visible from entrance, just keep moving
            if self.spotToParkIn == None:
                return self.position + 1
            else: 
                return self.stepTowards(self.spotToParkIn)
            
        else:
            # if no parking spot is visible, update visibility
            if self.spotToParkIn == None:
                self.visibility(self.position)
                self.spotToParkIn = self.closestVisibleSpot()
                if self.spotToParkIn == None:
                    return self.position + self.moveDir
            else:
                return self.stepTowards(self.spotToParkIn)
            
    def n_of_x(self):
        if self.spotToParkIn == None:
            # go far enough to see the first x spots
            if self.position < self.x - self.visionRange - 1:
                self.visibility(self.position)
                return self.position + 1
            
            # once we have seen the first x spots, we count the visible full spots
            elif self.position == self.x - self.visionRange - 1:
                self.visibility(self.position)
                counter = 0
                for i in range(self.x):
                    if self.knownSpots[i] == ParkingSpotState.FULL:
                        counter += 1
                # if it is very crowded (n/x or more) we move towards the best currently available spot
                if counter >= self.n:
                    self.spotToParkIn = self.closestVisibleSpot()
                    return self.stepTowards(self.spotToParkIn)
                else:
                    return self.position + 1

            # if we are past the visibility spot but still no goal in mind,
            # that means the parking lot is fairly empty so we keep moving to the end
            elif self.position < self.nSpotsInRow - self.visionRange - 1:
                self.visibility(self.position)
                return self.position + 1
            
            # we have arrived at the point where we can see the whole parking lot
            # so we just move to the spot closest to the store
            else: 
                self.visibility(self.position)
                self.spotToParkIn = self.closestVisibleSpot()
                return self.stepTowards(self.spotToParkIn)
        
        # if we already have a spot we're heading towards
        else: 
            return self.stepTowards(self.spotToParkIn)

    # run the strategy once and return the time it took to find a spot
    def run(self, timeLimit, strategy):
        time = 0.0
        while(not self.position == self.spotToParkIn):
            self.print_status(time)
            next_pos = strategy()
            if next_pos == self.position:
                self.print_status(time)
                print("done")
                return time
            time += self.move(next_pos)
            if time > timeLimit:
                return np.inf
        self.print_status(time)
        print("done")
        return time
    
    def print_status(self, time):
        print("Parking lot:")
        self.visualize()
        print("Current vision:")
        self.visualize_vision()
        print("Heading towards " + str(self.spotToParkIn))
        print("Time elapsed: " + str(time) + "\n")
    
    # run the strategy on the same graph 
    def test(self, timeLimit, iters=10):
        data = pd.DataFrame({'time': []})
        for i in range(iters):
            time = self.run(timeLimit)
            data.loc[i,'time'] = time
        print(data)

    def populate_bernoulli(self, p):
        for i in range(self.nSpotsInRow):
            self.matrix[i] = ParkingSpotState.FULL if random.random() < p else ParkingSpotState.EMPTY

    def visualize(self):
        #pprint(self.matrix)
        vis = []
        for i in range(len(self.matrix)):
            if self.matrix[i] == ParkingSpotState.EMPTY:
                vis.append("00" if self.position == i else "0")
            if self.matrix[i] == ParkingSpotState.FULL:
                vis.append("11" if self.position == i else "1")
            if self.matrix[i] == ParkingSpotState.UNKNOWN:
                vis.append("XX" if self.position == i else "X")
        print(vis)

    def visualize_vision(self):
        vis = []
        for i in range(len(self.knownSpots)):
            if self.knownSpots[i] == ParkingSpotState.EMPTY:
                vis.append("00" if self.position == i else "0")
            if self.knownSpots[i] == ParkingSpotState.FULL:
                vis.append("11" if self.position == i else "1")
            if self.knownSpots[i] == ParkingSpotState.UNKNOWN:
                vis.append("XX" if self.position == i else "X")
        print(vis)

m = ParkingMatrix(15, 5, 1)
m.populate_bernoulli(0.5)
m.n = 5
m.x = 6
#print(m.visualize())
#print(m.visualize_vision())
#print(m.bestVisibleSpot())
# m.run(20, m.n_of_x)
# m.run(20, m.backtrackStrategy)