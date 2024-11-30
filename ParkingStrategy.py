from Driver import Driver
from ParkingGraph import ParkingGraph
import numpy as np
import pandas as pd

class ParkingStrategy:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.G = self.driver.getGraph()

    # override/edit this to implement the rules that determine the next node to move to
    def determineNextPosition(self):
        pass

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

g = ParkingGraph(roadWidth=3, carWidth=2, carLength=5, nSpotsInRow=5, nBlocks=1)
g.initialize_basic()
g.populate_bernoulli(0.9)
g.visualize()

d = Driver(g.G, (1.5,1.5), (1.5,1.5), 10)

strat = ParkingStrategy(d)

strat.test(10)