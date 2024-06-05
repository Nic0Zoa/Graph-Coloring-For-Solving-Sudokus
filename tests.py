import numpy as np
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

class PlotGraph:
    def __init__(self, SubSize, UnsolvedSudoku, Solutions) -> None:
        self.SubSize = SubSize
        self.Solutions = Solutions
        self.UnsolvedSudoku = UnsolvedSudoku
        
        self.PlotSolutions()
        
    def AdjustPositions(self, pos):
        new_pos = {}
        for node, (x, y) in pos.items():
            new_pos[node] = (y, -x)
        return new_pos    
        
    def PlotSolutions(self):
        
        UnsolvedGraph = nx.sudoku_graph(self.SubSize)
        mapping = dict(zip(UnsolvedGraph.nodes(), self.Solutions[0].flatten()))
        pos = dict(zip(list(UnsolvedGraph.nodes()),
                   nx.grid_2d_graph(self.SubSize * self.SubSize, self.SubSize * self.SubSize)))
        pos = self.AdjustPositions(pos)
        
        low, *_, high = sorted(mapping.values())
        norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
        mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Pastel1)
        
        plt.figure(figsize=(8, 8))
        plt.title("Unsolved Sudoku")
        nx.draw(
            UnsolvedGraph,
            labels=mapping,
            pos=pos,
            with_labels=True,
            node_color=[mapper.to_rgba(i) for i in mapping.values()],
            width=1,
            node_size=1000,
        )
        plt.show()
        
        if len(self.Solutions) > 0:  
            if len(self.Solutions < 3):
                iterations = len(self.Solutions)
            else:
                iterations = 3
                            
            for i in range(iterations):
                SolvedGraph = nx.sudoku_graph(self.SubSize)
                mapping = dict(zip(SolvedGraph, self.Solutions[i].flatten()))
                pos = dict(zip(list(SolvedGraph.nodes()),
                        nx.grid_2d_graph(self.SubSize * self.SubSize, self.SubSize * self.SubSize)))
                pos = self.AdjustPositions(pos)
                
                plt.figure(figsize=(6, 6))
                nx.draw(
                    SolvedGraph,
                    labels=mapping,
                    pos=pos,
                    with_labels=True,
                    node_color=[mapper.to_rgba(i) for i in mapping.values()],
                    width=1,
                    node_size=1000,
                )
                plt.title("Sudoku #{}".format(i))
                plt.show()


    puzzle = np.asarray(
        [
            [1, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 3]
        ]
    )
solutions = []
solutions.append(puzzle)

PlotGraph(3, solutions)