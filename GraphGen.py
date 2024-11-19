import networkx as nx
import matplotlib.pyplot as plt

class GraphGen:
    def __init__(self, roadWidth, carWidth, carLength, nSpotsInRow, nBlocks):
        # Create a graph
        self.G = nx.Graph()
        self.lotWidth = 2*roadWidth + nSpotsInRow*carWidth

        GraphGen.addRow(False, 0.5*roadWidth, roadWidth, self.lotWidth, nSpotsInRow, carWidth, self.G)
        for i in range(nBlocks):
            GraphGen.addBlock(0.5*roadWidth + (i*(2*carLength+roadWidth)), roadWidth, carLength, self.lotWidth, nSpotsInRow, carWidth, self.G)
        
        # Visualize the graph
        pos = {node : node for node in self.G.nodes}
        nx.draw(self.G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=8)
        plt.title("Parking Lot Graph")
        plt.show()

    def createRow(isParkingSpace, yOffset, roadWidth, lotWidth, nSpotsInRow, carWidth):
        # create row as auxiliary graph 
        M = nx.Graph()

        # leftmost and rightmost vertex
        M.add_node((roadWidth/2, yOffset), isParkingSpace = False)
        M.add_node((lotWidth - roadWidth/2, yOffset), isParkingSpace = False)

        # middle vertices
        for i in range(nSpotsInRow):
            M.add_node((roadWidth + (i+0.5)*carWidth, yOffset), isParkingSpace = isParkingSpace)
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
        M = GraphGen.createRow(isParkingSpace, yOffset, roadWidth, lotWidth, nSpotsInRow, carWidth)
        G.add_nodes_from(M)
        G.add_edges_from(M.edges)

    # yOffset: the y coordinate of the vertices on the road directly below this block
    # assumes there is a road below
    def createBlock(yOffset, roadWidth, carLength, lotWidth, nSpotsInRow, carWidth):
        # create block as auxiliary graph 
        B = nx.Graph()

        r1 = GraphGen.createRow(True, yOffset + 0.5*roadWidth + 0.5*carLength, roadWidth, lotWidth, nSpotsInRow, carWidth)
        r2 = GraphGen.createRow(True, yOffset + 0.5*roadWidth + 1.5*carLength, roadWidth, lotWidth, nSpotsInRow, carWidth)
        r3 = GraphGen.createRow(False, yOffset + roadWidth + 2*carLength, roadWidth, lotWidth, nSpotsInRow, carWidth)

        B.add_nodes_from(r1)
        B.add_nodes_from(r2)
        B.add_nodes_from(r3)
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
        M = GraphGen.createBlock(yOffset, roadWidth, carLength, lotWidth, nSpotsInRow, carWidth)

        G.add_nodes_from(M)
        G.add_edges_from(M.edges)

        G.add_edge((roadWidth/2, yOffset), 
                        (roadWidth/2, yOffset + 0.5*roadWidth + 0.5*carLength))
        G.add_edge((lotWidth - roadWidth/2, yOffset), 
                        (lotWidth - roadWidth/2, yOffset + 0.5*roadWidth + 0.5*carLength))

        for i in range(nSpotsInRow):
            G.add_edge((roadWidth + (i+0.5)*carWidth, yOffset), 
                            (roadWidth + (i+0.5)*carWidth, yOffset + 0.5*roadWidth + 0.5*carLength))

GraphGen(roadWidth=3, carWidth=2, carLength=5, nSpotsInRow=5, nBlocks=3)