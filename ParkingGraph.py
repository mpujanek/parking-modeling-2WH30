import networkx as nx
import matplotlib.pyplot as plt
from ParkingSpotState import ParkingSpotState

class ParkingGraph:
    def __init__(self, roadWidth, carWidth, carLength, nSpotsInRow, nBlocks):
        self.roadWidth = roadWidth
        self.carWidth = carWidth
        self.carLength = carLength
        self.nSpotsInRow = nSpotsInRow
        self.nBlocks = nBlocks

        self.G = nx.Graph()
        self.lotWidth = 2*roadWidth + nSpotsInRow*carWidth

    def initialize(self):
        ParkingGraph.addRow(False, 0.5*self.roadWidth, self.roadWidth, self.lotWidth, self.nSpotsInRow, self.carWidth, self.G)
        for i in range(self.nBlocks):
            ParkingGraph.addBlock(0.5*self.roadWidth + (i*(2*self.carLength+self.roadWidth)), self.roadWidth, self.carLength, self.lotWidth, self.nSpotsInRow, self.carWidth, self.G)
    
    def initialize_basic(self):
        self.initialize()
        nodes_to_remove = [node for node in self.G.nodes if node[1]>6]
        self.G.remove_nodes_from(nodes_to_remove)

    def visualize(self):
        # Visualize the graph
        pos = {node : node for node in self.G.nodes}
        node_colors = [
            'red' if self.G.nodes[node].get('isParkingSpace', False) else 'skyblue'
            for node in self.G.nodes
        ]
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=8)
        plt.title("Parking Lot Graph")
        plt.show()

    def createRow(isParkingSpace, yOffset, roadWidth, lotWidth, nSpotsInRow, carWidth):
        # create row as auxiliary graph 
        M = nx.Graph()

        # leftmost and rightmost vertex
        M.add_node((roadWidth/2, yOffset), isParkingSpace = False, state = ParkingSpotState.EMPTY)
        M.add_node((lotWidth - roadWidth/2, yOffset), isParkingSpace = False, state = ParkingSpotState.EMPTY)

        # middle vertices
        for i in range(nSpotsInRow):
            M.add_node((roadWidth + (i+0.5)*carWidth, yOffset), isParkingSpace = isParkingSpace, state = ParkingSpotState.EMPTY)
            if (not isParkingSpace):
                if (i == 0):
                    M.add_edge((roadWidth/2, yOffset), (roadWidth + (i+0.5)*carWidth, yOffset))
                elif (i == nSpotsInRow - 1):
                    M.add_edge((roadWidth + (i+0.5)*carWidth, yOffset), (lotWidth - roadWidth/2, yOffset))
                    M.add_edge((roadWidth + (i+0.5)*carWidth, yOffset), (roadWidth + (i-0.5)*carWidth, yOffset))
                else:
                    M.add_edge((roadWidth + (i+0.5)*carWidth, yOffset), (roadWidth + (i-0.5)*carWidth, yOffset))

        return M
    
    # add row to main graph
    def addRow(isParkingSpace, yOffset, roadWidth, lotWidth, nSpotsInRow, carWidth, G):
        M = ParkingGraph.createRow(isParkingSpace, yOffset, roadWidth, lotWidth, nSpotsInRow, carWidth)
        G.add_nodes_from(M.nodes(data=True))
        G.add_edges_from(M.edges)

    # yOffset: the y coordinate of the vertices on the road directly below this block
    # assumes there is a road below
    def createBlock(yOffset, roadWidth, carLength, lotWidth, nSpotsInRow, carWidth):
        # create block as auxiliary graph 
        B = nx.Graph()

        r1 = ParkingGraph.createRow(True, yOffset + 0.5*roadWidth + 0.5*carLength, roadWidth, lotWidth, nSpotsInRow, carWidth)
        r2 = ParkingGraph.createRow(True, yOffset + 0.5*roadWidth + 1.5*carLength, roadWidth, lotWidth, nSpotsInRow, carWidth)
        r3 = ParkingGraph.createRow(False, yOffset + roadWidth + 2*carLength, roadWidth, lotWidth, nSpotsInRow, carWidth)

        B.add_nodes_from(r1.nodes(data=True))
        B.add_nodes_from(r2.nodes(data=True))
        B.add_nodes_from(r3.nodes(data=True))
        B.add_edges_from(r1.edges)
        B.add_edges_from(r2.edges)
        B.add_edges_from(r3.edges)

        for a,b in zip(r2.nodes, r3.nodes):
            B.add_edge(a,b)

        B.add_edge((roadWidth/2, yOffset + 0.5*roadWidth + 0.5*carLength), 
                    (roadWidth/2, yOffset + 0.5*roadWidth + 1.5*carLength))
        B.add_edge((lotWidth - roadWidth/2, yOffset + 0.5*roadWidth + 0.5*carLength), 
                    (lotWidth - roadWidth/2, yOffset + 0.5*roadWidth + 1.5*carLength))

        return B
    
    # add block to main graph
    def addBlock(yOffset, roadWidth, carLength, lotWidth, nSpotsInRow, carWidth, G):
        M = ParkingGraph.createBlock(yOffset, roadWidth, carLength, lotWidth, nSpotsInRow, carWidth)

        G.add_nodes_from(M.nodes(data=True))
        G.add_edges_from(M.edges)

        G.add_edge((roadWidth/2, yOffset), 
                        (roadWidth/2, yOffset + 0.5*roadWidth + 0.5*carLength))
        G.add_edge((lotWidth - roadWidth/2, yOffset), 
                        (lotWidth - roadWidth/2, yOffset + 0.5*roadWidth + 0.5*carLength))

        for i in range(nSpotsInRow):
            G.add_edge((roadWidth + (i+0.5)*carWidth, yOffset), 
                            (roadWidth + (i+0.5)*carWidth, yOffset + 0.5*roadWidth + 0.5*carLength))

g = ParkingGraph(roadWidth=3, carWidth=2, carLength=5, nSpotsInRow=5, nBlocks=1)
g.initialize_basic()
g.visualize()