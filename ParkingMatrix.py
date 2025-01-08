import numpy as np
from ParkingSpotState import ParkingSpotState
from pprint import pprint
import random
import pandas as pd

class ParkingMatrix:

    def __init__(self, nSpotsInRow, visionRange, drivingSpeed, walkingSpeed):
        # factor = 3 if doubleRows else 2
        self.nSpotsInRow = nSpotsInRow
        self.knownSpots = [ParkingSpotState.UNKNOWN] * nSpotsInRow
        self.position = 0
        self.visionRange = visionRange
        self.drivingSpeed = drivingSpeed
        self.walkingSpeed = walkingSpeed
        # extra stuff to use in strategy
        self.spotToParkIn = None
        self.moveDir = 1
        self.n = 0
        self.x = 0
        self.backTrack = False
        self.fraction = 1/3
        #self.matrix = [[ParkingSpotState.ROAD if (x==0 or x==nspotsInRow+1 or y %factor == 0) else ParkingSpotState.EMPTY for x in range(nspotsInRow + 2)] for y in range(factor*nBlocks+1)]
        self.matrix = [ParkingSpotState.EMPTY] * nSpotsInRow

    def getMatrix(self):
        return self.matrix
    
    
    def visibility(self, position):
        for i in range(0, self.visionRange + 1):
            if position + i < self.nSpotsInRow:
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


    #Park in the first available spot, will go out of bounds on a full parking lot.
    def firstSpotStrategy(self):
        if self.matrix[self.position] == ParkingSpotState.EMPTY:
            self.spotToParkIn = self.position
            return self.position
        return self.position + 1

    def backtrackStrategy(self):

        if self.position == 0 and self.backTrack:
            return self.position

        if self.position == len(self.matrix) - 1:
            self.backTrack = True

        if not self.backTrack:
            return self.position + 1
        
        else:
            if self.matrix[self.position] == ParkingSpotState.EMPTY:
                self.spotToParkIn = self.position
                return self.position
            return self.position - 1

            
    #Parks in the best visible spot after fraction of cars.
    def parkAfterFractionStrategy(self):

        if (self.position >= len(self.matrix) - 1 or self.backTrack):
            self.backTrack = True
            return self.backtrackStrategy()

        #print("fraction = " + str((self.position / len(self.matrix))))
        
        if (self.position / len(self.matrix) >= self.fraction):
            return self.bestVisibleSpot()
        
        return self.position + 1

        

    def walkToEnd(self, position):
        distance = float(len(self.matrix) - position)
        return distance / float(self.walkingSpeed)

    # assumes there is a parking spot available and no changes in parked cars
    def bestVisibleSpot(self):
        # update visibility
        self.visibility(self.position)

        # determine furthest empty spot visible from entrance
        self.spotToParkIn = self.closestVisibleSpot()

        # if no empty spot visible from entrance, just keep moving
        if self.spotToParkIn == None:
            return self.position + 1
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
                # (or keep moving if no such spot exists)
                if counter >= self.n:
                    self.spotToParkIn = self.closestVisibleSpot()
                    return self.stepTowards(self.spotToParkIn) if not self.spotToParkIn == None else self.position + 1
                # if it is not crowded we keep moving until the end of the parking lot
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
            self.spotToParkIn = self.closestVisibleSpot()
            return self.stepTowards(self.spotToParkIn)

    # run the strategy once and return the time it took to find a spot
    def run_and_print(self, timeLimit, strategy):
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
    
        # run the strategy once and return the time it took to find a spot
    
    def run(self, timeLimit, strategy):
        time = 0.0
        while(not self.position == self.spotToParkIn):
            next_pos = strategy()
            if next_pos == self.position:
                time += self.walkToEnd(self.position)
                return time
            time += self.move(next_pos)
            if time > timeLimit:
                return np.inf
        time += self.walkToEnd(self.position)
        return time
    
    def print_status(self, time):
        print("Parking lot:")
        self.visualize()
        print("Current vision:")
        self.visualize_vision()
        print("Heading towards " + str(self.spotToParkIn))
        print("Time elapsed: " + str(time) + "\n")
    
    # run the strategy many times and export time it took
    def test(self, timeLimit, strategies, populate, param, iters=10):
        # initialize the dataframe 
        data = pd.DataFrame()
        for strategy in strategies:
            data[strategy.__name__] = pd.Series(dtype=float)

        # run the simulation
        for i in range(iters):
            # populate parking lot, making sure there is at least one available spot
            populate(param)
            while self.matrix == [ParkingSpotState.FULL for x in range(self.nSpotsInRow)]:
                populate(param)

            # run strategy and record time
            for strategy in strategies:
                # reset position and knowledge
                self.position = 0
                self.knownSpots = [ParkingSpotState.UNKNOWN] * self.nSpotsInRow
                self.spotToParkIn = None
                self.backTrack = False
                time = self.run(timeLimit, strategy)
                data.loc[i,strategy.__name__] = time
        return data.describe()
        #print(data)
        #print(data.describe())

    def populate_bernoulli(self, b):
        p = b / self.nSpotsInRow
        for i in range(self.nSpotsInRow):
            self.matrix[i] = ParkingSpotState.FULL if random.random() < p else ParkingSpotState.EMPTY

    # p_max: probability that the spot closest to the store is occupied,
    # then the probability falls off exponentially
    # steepness: exponent of the probability dropoff curve
    def populate_exponential(self, b, steepness=1):
        n = self.nSpotsInRow
        for i in range(self.nSpotsInRow):
            # get p value for bernoulli from exponential distribution
            threshold = np.exp(-(n - i) / (1 + b)) 

            # bernoulli
            self.matrix[i] = ParkingSpotState.FULL if random.random() < threshold else ParkingSpotState.EMPTY

    # this one drops off linearly
    def populate_linear(self, p_min, p_max=1):
        n = self.nSpotsInRow
        for i in range(self.nSpotsInRow):
            # linear interpolation between p_max and p_min
            threshold = (i/n) * p_max + (1 - i/n) * p_min
            self.matrix[i] = ParkingSpotState.FULL if random.random() < threshold else ParkingSpotState.EMPTY

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

m = ParkingMatrix(100, 1, 1, 0.5)
#m.populate_bernoulli(0.9)
m.n = 19
m.x = 20
#print(m.visualize())
#print(m.visualize_vision())
#print(m.bestVisibleSpot())
#m.run_and_print(50, m.n_of_x)
strategies = [m.bestVisibleSpot, m.n_of_x, m.parkAfterFractionStrategy, 
             m.backtrackStrategy, m.firstSpotStrategy]
#m.test(1000, strategies, m.populate_exponential, 80, 1000)

# test a spread of parameters
df_expectation_1 = pd.DataFrame()
df_std_1 = pd.DataFrame()
for strategy in strategies:
    df_expectation_1[strategy.__name__] = pd.Series(dtype=float)
    df_std_1[strategy.__name__] = pd.Series(dtype=float)
for b in range(100):
    df_b = m.test(1000, strategies, m.populate_bernoulli, b, iters=100)
    df_expectation_1.loc[b] = df_b.loc['mean']
    df_std_1.loc[b] = df_b.loc['std']

df_expectation_2 = pd.DataFrame()
df_std_2 = pd.DataFrame()
for strategy in strategies:
    df_expectation_2[strategy.__name__] = pd.Series(dtype=float)
    df_std_2[strategy.__name__] = pd.Series(dtype=float)
for b in range(100):
    df_b = m.test(1000, strategies, m.populate_exponential, b, iters=100)
    df_expectation_2.loc[b] = df_b.loc['mean']
    df_std_2.loc[b] = df_b.loc['std']


import matplotlib.pyplot as plt

B=range(100)

fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

# first available spot strategy
axs[0].scatter(B, df_std_1['firstSpotStrategy'], label="distance independent")
axs[0].scatter(B, df_std_2['firstSpotStrategy'], label="distance dependent")
axs[0].set_title("First available spot")
axs[0].set_xlabel("busyness, b")
axs[0].legend(loc="best")
axs[0].set_ylabel("Variance of total time, V[T^t]")

# greedy strategy
axs[1].scatter(B, df_std_1['backtrackStrategy'], label="distance independent")
axs[1].scatter(B, df_std_2['backtrackStrategy'], label="distance dependent")
axs[1].set_title("Greedy strategy")
axs[1].set_xlabel("busyness, b")
axs[1].legend(loc="best")
#axs[1].set_ylabel("E[T^t]")

# best visible spot strategy
axs[2].scatter(B, df_std_1['bestVisibleSpot'], label="distance independent")
axs[2].scatter(B, df_std_2['bestVisibleSpot'], label="distance dependent")
axs[2].set_title("Best visible spot")
axs[2].set_xlabel("busyness, b")
axs[2].legend(loc="best")
#axs[2].set_ylabel("E[T^t]")
#axs[2].set_ylim(-10, 10)  # Limit y-axis for better visibility

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()

