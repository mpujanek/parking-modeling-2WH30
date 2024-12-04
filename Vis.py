from ParkingMatrix import ParkingMatrix
import networkx as nx
from ParkingSpotState import ParkingSpotState
from enum import Enum
from pprint import pprint
from copy import deepcopy

class cardinal(Enum):

    def __getItem__(self, index):
        return cardinal.index.value

    NORTH = [-1,0]
    WEST = [0,1]
    SOUTH = [1,0]
    EAST = [0,-1]

class Vis:


    def __init__(self, M: ParkingMatrix):
        self.M = M.getMatrix()

        #Instantiate dictionary of each cell.
        self.kb = {}
        for i in range(len(self.M[0])):
            for j in range(len(self.M)):
                pos = self.posToNumber(j, i)
                self.kb[pos] = ParkingSpotState.UNKNOWN             

    def posToNumber(self, row, col):
        return row * len(self.M[0]) + col

    #Returns the directions we need to explore.
    def getDirections(self, position):
        ExploreDirections = []
        xpos = position[0]
        ypos = position[1]

        if self.M[xpos][ypos + 1] == ParkingSpotState.ROAD and ypos != 0:
            ExploreDirections.append(cardinal.NORTH) 
        
        if self.M[xpos + 1][ypos] == ParkingSpotState.ROAD and xpos != len(self.M) - 1:
            ExploreDirections.append(cardinal.WEST)

        if self.M[xpos][ypos - 1] == ParkingSpotState.ROAD and ypos != len(self.M) - 1:
            ExploreDirections.append(cardinal.SOUTH)
        
        if self.M[xpos - 1][ypos] == ParkingSpotState.ROAD and xpos != 0:
            ExploreDirections.append(cardinal.WEST)

        return ExploreDirections

        

    def isValidCoordinate(self, row, col):
        if row < 0 or row >= len(self.M):
            return False
        if col < 0 or col >= len(self.M[0]):
            return False
        return True
    
    def moveCar(self, position, dir : cardinal):
        position[0] += dir.value[0]
        position[1] += dir.value[1]
    
    def getCelState(self, position, dir : cardinal):
        pos = deepcopy(position)
        pos[0] += dir.value[0]
        pos[1] += dir.value[1]
        spotToCheck = self.M[pos[0]][pos[1]]
        return spotToCheck


    # Will run a BFS to find the first visible cars.
    def getNewCars(self, position):

        #Will contain any newly discovered parkingspots
        newCars = []

        directions = self.getDirections(position)

        for direction in directions:
            lookDir = [[True, True],[True, True]]

            pos = deepcopy(position)
            self.moveCar(pos, direction)
            while(self.isValidCoordinate(pos[0], pos[1])):
                for dir in cardinal:
                    if lookDir[dir.value[0]][dir.value[1]] != False:
                        if self.isValidCoordinate(pos[0] + dir.value[0], pos[1] + dir.value[1]):
                            if self.getCelState(pos, dir) == ParkingSpotState.EMPTY:
                                newCars.append([pos[0] + dir.value[0], pos[1] + dir.value[1]])
                            else:
                                lookDir[dir.value[0]][dir.value[1]] == False
                self.moveCar(pos, direction)

        unique = [x for i, x in enumerate(newCars) if i == newCars.index(x)]
        return unique
    
v = Vis(ParkingMatrix(6,2, True))
print(v.getNewCars([0,0]))
