from Abstract_Strategy import Abstract_Strategy
from Abstract_ProbDist import Abstract_ProbDist
from Matrix import PMatrix
from ParkingSpotState import ParkingSpotState
from Backtrack_Strategy import BackTrack_Strategy
from Best_Visible_Strategy import BestVisibleSpotStrategy
from n_of_x_Strategy import n_of_x_Strategy
from SimpleVis import SimpleVis
from Bernouli_ProbDist import Bernouli_ProbDist
import math

class Simulation:

    def __init__(self, Strategy : Abstract_Strategy, parkingMatrix : PMatrix, drivingSpeed = 0.5, walkingSpeed = 1, timeOut = 99999999, verbose = True):
        self.drivingSpeed = drivingSpeed
        self.walkingSpeed = walkingSpeed
        self.pMatrix = parkingMatrix
        Strategy.setMatrix(self.pMatrix.getMatrix())
        self.Strategy = Strategy
        self.timeOut = timeOut
        self.verbose = verbose
        self.score = self.simulate()

    def getInfo(self) -> dict:
        return {'score': self.score}

    def simulate(self) -> int:
        if self.verbose: print(str(type(self.Strategy).__name__))
        pos = 0
        steps = 0
        for i in range(self.timeOut):
            #Print parking- and vismatrices
            if self.verbose:
                self.print_status(i, pos)

            #Advance the strategy.
            posOld = pos
            pos = self.Strategy.getNextStep()
            if posOld != pos:
                steps += 1

            if self.Strategy._isFinished():
                score = self.calculateScore(steps, pos)
                if self.verbose:
                    self.print_status(i + 1, pos)
                    print(str(score))
                return score
                
        raise ValueError("Timeout on: " + type(self.Strategy).__name__)



    def calculateScore(self, spotsDriven : int, pos : int) -> float:
        return spotsDriven * self.drivingSpeed + (len(self.pMatrix.getMatrix()) - pos - 1) * self.walkingSpeed


    def print_status(self, time : int, pos : int):
        print("Parking lot:")
        self.visualize(self.pMatrix.getMatrix(), pos)
        print("Current vision:")
        self.visualize(self.Strategy.getVisibility(), pos)
        print("Time elapsed: " + str(time) + "\n")

    def visualize(self, matrix : list, pos : int):
        toPrint = []
        for i in range(len(matrix)):
            if matrix[i] == ParkingSpotState.EMPTY:
                toPrint.append("00" if pos == i else "0")
            if matrix[i] == ParkingSpotState.FULL:
                toPrint.append("11" if pos == i else "1")
            if matrix[i] == ParkingSpotState.UNKNOWN:
                toPrint.append("XX" if pos == i else "X")
        print(toPrint)


# parkingMatrix = PMatrix(10, Bernouli_ProbDist())
# Simulation(n_of_x_Strategy(SimpleVis(), 0.3, 3), parkingMatrix, timeOut=20)