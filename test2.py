import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def AdjustPositions(pos):
    new_pos = {}
    for node, (x, y) in pos.items():
        new_pos[node] = (y, -x)
    return new_pos

puzzle = np.asarray(
    [
        [1, 0, 0, 0],
        [2, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 3]
    ]
)

n = 2
G = nx.sudoku_graph(n)
mapping = dict(zip(G.nodes(), puzzle.flatten()))
pos = dict(zip(list(G.nodes()), nx.grid_2d_graph(n * n, n * n)))
post = AdjustPositions(pos)
# we map the nodes 1-9 to a colormap
unique_labels = list(set(puzzle.flatten()))
colors = mpl.cm.get_cmap('Pastel1', len(unique_labels))

plt.figure(figsize=(8, 8))
plt.title("Unsolved Sudoku")
nx.draw(
    G,
    labels=mapping,
    pos=pos,
    with_labels=True,
    node_color=[colors(unique_labels.index(mapping[node]))
                for node in G.nodes()],
    width=1,
    node_size=1000,
)
plt.show()

puzzle = np.asarray(
    [
        [1, 4, 3, 2],
        [2, 3, 4, 1],
        [3, 1, 2, 4],
        [4, 2, 1, 3]
    ]
)
A = nx.sudoku_graph(n)
mapping = dict(zip(A.nodes(), puzzle.flatten()))
pos = dict(zip(list(A.nodes()), nx.grid_2d_graph(n * n, n * n)))
post = AdjustPositions(pos)
plt.figure(figsize=(8, 8))
plt.title("Unsolasdasdasd")
nx.draw(
    G,
    labels=mapping,
    pos=pos,
    with_labels=True,
    node_color=[colors(unique_labels.index(mapping[node]))
                for node in A.nodes()],
    width=1,
    node_size=1000,
)
plt.show()



