# Graph Coloring for Solving Sudokus
## Introduction

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Is there any way to compute the solution of a sudoku before trying to solving it? If so, how many ways can it be solved? Will always be there a solution?


The main algorithm that you can find in these repository contains a way to anwers these questions. Using graph theory, there is a way to compute the solution of every $$n^2 \times n^2$$ sudoku, at least that's what I coded.

The main theory behind this code is [Graph Coloring](https://en.wikipedia.org/wiki/Graph_coloring), which basically consists of assigning colors to the graph, in this case to the vertex, so two adjacent vertex don't have the same color.
In our case, each number, from $$1$$ to $$n$$ represents a color, and using some techniques, we can build a graph from the sudoku grid, which is constructed once you specify the desired size.
Combining graph coloring with a simple [Backtracking](https://en.wikipedia.org/wiki/Backtracking) algorithm this code can find if any sudoku you type has:
- Unique solution
- Doesn't have a solution
- Multiple Solution

But backtracking is expensive, so, if you typed just a few numbers or your grid is very large, well, you'll have to wait. Even if it is ten times longer than the universe lifespan.

Given that this is only made for fun an research purposes, this code does not include any executable file, nor interface, but you can give it a try on your favorite python compiler.


## Bonus

I also included some files that I created during the creative process, just for fun.

