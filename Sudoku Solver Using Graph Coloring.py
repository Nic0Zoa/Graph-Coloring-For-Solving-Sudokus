import os
import math
import numpy as np
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

class SudokuSolver:
    def __init__(self, sudokuSize) -> None:
        self.Size = sudokuSize
        self.SolutionsNumber = 0
        self.PrintUnsolved = False
        self.SubSize = int(math.sqrt(sudokuSize))
        self.SupSize = int(math.pow(sudokuSize, 2))

        self.VertexColor = np.zeros(self.SupSize, dtype=int)
        self.Colors = np.asarray([i + 1 for i in range(self.Size)], dtype=int)

        self.AdjacencyList = dict({i: [] for i in range(self.SupSize)})
        self.AdjacencyMatrix = np.zeros((self.SupSize, self.SupSize), dtype=int)

        self.auxPivotVector = np.zeros(self.SupSize, dtype=int)
        self.auxVertexMatrix = np.asarray([[i + self.Size*k for i in range(self.Size)] for k in range(self.Size)])

        self.Solutions = []
        self.Sudoku = np.zeros((self.Size, self.Size), dtype=object)
        self.UnsolvedSudoku = np.zeros((self.Size, self.Size), dtype=object)
        
        self.SolveSudoku()

    def fill(self):
        for i in range(self.Size):
            for j in range(self.Size):
                print("The ↓ marks the position where you are\n")
                self.Sudoku[i][j] = '↓'
                self.printSudoku()
                Element = input("\nType the element of the row {} and column {} (If there's no element, type 0): ".format(i+1, j+1))
                os.system('cls')

                while (int(Element) < 0 or int(Element) > self.Size):
                    print("\nThe ↓ marks the position where you are\n")
                    self.printSudoku()
                    print("\nType a valid value\n")
                    Element = input(
                        "Type the element of the row {} and column {} (If there's no element, type 0): ".format(i+1, j+1))
                    os.system('cls')

                self.Sudoku[i][j] = int(Element)
                self.UnsolvedSudoku[i][j] = int(Element)
                os.system('cls')
                                
    def printSudoku(self):
        for i in range(self.Size):
            for j in range(self.Size):
                if (i + 1) % self.SubSize == 1 and j == 0 and i != 0:
                    print("-"*(3*self.Size + self.SubSize - 1))
                if j == self.Size - 1:
                    print("", self.Sudoku[i][j])
                else:
                    print("", self.Sudoku[i][j], end=" ")
                    if j % self.SubSize == self.SubSize - 1:
                        print("|", end="")

    def preColor(self):
        Vertex = 0
        for i in range(self.Size):
            for j in range(self.Size):
                if self.Sudoku[i][j] != 0:
                    self.VertexColor[Vertex] = self.Sudoku[i][j]
                    self.auxPivotVector[Vertex] = 1
                Vertex += 1

    def isEdge(self, V1, V2):
        if self.AdjacencyMatrix[V1][V2] == 1:
            return True
        return False

    def isSafe(self, Vertex, Color):
        for V in self.AdjacencyList[Vertex]:
            if self.VertexColor[V] == Color:
                return False
        return True

    def addEdge(self, V1, V2):
        if not self.isEdge(V1, V2):
            if V1 != V2:
                self.AdjacencyMatrix[V1][V2] = 1
                self.AdjacencyMatrix[V2][V1] = 1
                self.AdjacencyList[V1].append(V2)
                self.AdjacencyList[V2].append(V1)
            else:
                self.AdjacencyMatrix[V1][V1] = 1
                self.AdjacencyList[V1].append(V1)

    def addConections(self):
        for i in range(self.Size):
            for j in range(self.Size):
                Vertex = self.auxVertexMatrix[i][j]
                RelativeRowPos = i % self.SubSize
                RelativeRowCol = j % self.SubSize

                for n in range(self.Size):
                    SameRow = self.auxVertexMatrix[i][n]
                    SameCol = self.auxVertexMatrix[n][j]
                    if SameRow != Vertex:
                        self.addEdge(Vertex, SameRow)
                    if SameCol != Vertex:
                        self.addEdge(Vertex, SameCol)

                for SubRow in range(self.SubSize):
                    for SubCol in range(self.SubSize):
                        RowDistance = abs(RelativeRowPos - SubRow)
                        ColDistance = abs(RelativeRowCol - SubCol)
                        if SubRow < RelativeRowPos:
                            if SubCol > RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i - RowDistance][j + ColDistance]
                                self.addEdge(Vertex, valueInGrid)
                            if SubCol < RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i - RowDistance][j - ColDistance]
                                self.addEdge(Vertex, valueInGrid)
                        elif SubRow > RelativeRowPos:
                            if SubCol > RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i + RowDistance][j + ColDistance]
                                self.addEdge(Vertex, valueInGrid)
                            if SubCol < RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i + RowDistance][j - ColDistance]
                                self.addEdge(Vertex, valueInGrid)

    def coloring(self, Vertex):
        if self.SolutionsNumber > 10:
            return 0

        elif Vertex == self.SupSize:
            for i in range(self.SupSize):
                row = int(i/self.Size)
                col = i % self.Size
                self.Sudoku[row][col] = self.VertexColor[i]

            flag = True
            for V in self.VertexColor:
                if not self.isSafe(V, self.VertexColor[V]):
                    flag = False
                    break
            if flag == True:
                self.SolutionsNumber += 1
                self.printSolutions()

        else:
            if self.auxPivotVector[Vertex] == 1:
                self.coloring(Vertex + 1)
            else:
                for Color in self.Colors:
                    if self.isSafe(Vertex, Color):
                        self.VertexColor[Vertex] = Color
                        self.coloring(Vertex + 1)
                        self.VertexColor[Vertex] = -1

    def printSolutions(self):
        if self.SolutionsNumber == 0:
            print("Unsolved Sudoku: ")
            print("\nThere are no solutions to print\n")
            PlotGraph(self.SubSize, self.UnsolvedSudoku, 0, False, False)
        else:
            if self.PrintUnsolved == False:
                print("Unsolved Sudoku: \n")
                PlotGraph(self.SubSize, self.UnsolvedSudoku, 0, False, False)
                self.PrintUnsolved = True
                print("")
            print("")
            print("*"*(5*self.Size + self.SubSize))
            self.printSudoku()
            print("")
            PlotGraph(self.SubSize, self.UnsolvedSudoku, self.Sudoku, True, True)
            

    def SolveSudoku(self):
        self.fill()
        self.preColor()
        self.addConections()
        self.coloring(0)
        if self.SolutionsNumber == 1:
            print("\nThe given sudoku has unique solution\n")
        elif self.SolutionsNumber > 10:
            print("\nYou have more than 10 solutions available\n")
        else:
            print("\nYou have {} solutions\n".format(self.SolutionsNumber))


class PlotGraph:
    def __init__(self, SubSize, UnsolvedSudoku, Solution, Solutions, PrintedUnsolved) -> None:
        self.SubSize = SubSize
        self.Solution = Solution
        self.Solutions = Solutions
        self.UnsolvedSudoku = UnsolvedSudoku
        self.PrintedUnsolved = PrintedUnsolved

        self.PlotSolutions()

    def AdjustPositions(self, pos):
        AdjPos = {}
        for node, (x, y) in pos.items():
            AdjPos[node] = (y, -x)
        return AdjPos

    def PlotSolutions(self):
        UnsolvedGraph = nx.sudoku_graph(self.SubSize)
        mapping = dict(zip(UnsolvedGraph.nodes(),
                       self.UnsolvedSudoku.flatten()))
        pos = dict(zip(list(UnsolvedGraph.nodes()),
                   nx.grid_2d_graph(self.SubSize * self.SubSize, self.SubSize * self.SubSize)))
        pos = self.AdjustPositions(pos)

        low, *_, high = sorted(mapping.values())
        norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
        mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.Pastel1)

        if not self.PrintedUnsolved:
            
            plt.figure(figsize=(6, 6))
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

        if self.Solutions:
            SolvedGraph = nx.sudoku_graph(self.SubSize)
            mapping = dict(zip(SolvedGraph, self.Solution.flatten()))
            pos = dict(zip(list(SolvedGraph.nodes()),
                            nx.grid_2d_graph(self.SubSize * self.SubSize, self.SubSize * self.SubSize)))
            pos = self.AdjustPositions(pos)

            plt.figure(figsize=(6, 6))
            plt.title("Possible Solution")
            nx.draw(
                SolvedGraph,
                labels=mapping,
                pos=pos,
                with_labels=True,
                node_color=[mapper.to_rgba(i) for i in mapping.values()],
                width=1,
                node_size=1000,
            )
            plt.show()


os.system('cls')
Size = int(input("Type the size of your sudoku (e.g. if it is a 4x4 sudoku, type 4, 9x9, type 9, etc): "))
Sudoku = SudokuSolver(Size)

