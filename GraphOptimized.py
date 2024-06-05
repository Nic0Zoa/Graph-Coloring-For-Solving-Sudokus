import numpy as np
import math

class SudokuSolver:
    def __init__(self, sudokuSize) -> None:

        self.Size = sudokuSize
        self.SolutionsNumber = 0
        self.SubSize = int(math.sqrt(sudokuSize))
        self.SupSize = int(math.pow(sudokuSize, 2))

        self.VertexColor = np.zeros(self.SupSize, dtype=int)
        self.Colors = np.asarray([i + 1 for i in range(self.Size)], dtype=int)

        self.AdjacencyList = dict({i: [] for i in range(self.SupSize)})
        self.AdjacencyMatrix = np.zeros(
            (self.SupSize, self.SupSize), dtype=int)

        self.auxPivotVector = np.zeros(self.SupSize, dtype=int)
        self.auxVertexMatrix = np.asarray(
            [[i + self.Size*k for i in range(self.Size)] for k in range(self.Size)])

        self.Solutions = []
        self.Sudoku = np.zeros((self.Size, self.Size), dtype=int)

        self.SolveSudoku()
                
    def fill(self):
        for i in range(self.Size):
            for j in range(self.Size):
                self.Sudoku[i][j] = int(input("Type the element of the row {} and column {} (If there's no element, type 0): ".format(i+1,j+1)))            
                
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
                valueInPosition = self.auxVertexMatrix[i][j]
                RelativeRowPos = i % self.SubSize
                RelativeRowCol = j % self.SubSize

                for n in range(self.Size):
                    SameRow = self.auxVertexMatrix[i][n]
                    SameCol = self.auxVertexMatrix[n][j]
                    if SameRow != valueInPosition:
                        self.addEdge(valueInPosition, SameRow)
                    if SameCol != valueInPosition:
                        self.addEdge(valueInPosition, SameCol)

                for SubRow in range(self.SubSize):
                    for SubCol in range(self.SubSize):
                        RowDistance = abs(RelativeRowPos - SubRow)
                        ColDistance = abs(RelativeRowCol - SubCol)
                        if SubRow < RelativeRowPos:
                            if SubCol > RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i -
                                                                   RowDistance][j + ColDistance]
                                self.addEdge(valueInPosition, valueInGrid)
                            if SubCol < RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i -
                                                                   RowDistance][j - ColDistance]
                                self.addEdge(valueInPosition, valueInGrid)
                        elif SubRow > RelativeRowPos:
                            if SubCol > RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i +
                                                                   RowDistance][j + ColDistance]
                                self.addEdge(valueInPosition, valueInGrid)
                            if SubCol < RelativeRowCol:
                                valueInGrid = self.auxVertexMatrix[i +
                                                                   RowDistance][j - ColDistance]
                                self.addEdge(valueInPosition, valueInGrid)

    def coloring(self, Vertex):
        if Vertex == self.SupSize:
            for i in range(self.SupSize):
                row = int(i/self.Size)
                col = i % self.Size
                self.Sudoku[row][col] = self.VertexColor[i]
                
            self.SolutionsNumber += 1
            self.Solutions.append(self.Sudoku)
        else:
            if self.auxPivotVector[Vertex] == 1:
                self.coloring(Vertex + 1)
            else:
                for Color in self.Colors:
                    if self.isSafe(Vertex, Color):
                        self.VertexColor[Vertex] = Color
                        self.coloring(Vertex + 1)
                        self.VertexColor[Vertex] = -1

    def SolveSudoku(self):
        self.fill()
        self.preColor()
        self.addConections()
        self.coloring(0)
        
        print("You have {} solutions".format(self.SolutionsNumber))
        

Sudoku4x4 = SudokuSolver(4)
        

print(Sudoku4x4.Sudoku)

