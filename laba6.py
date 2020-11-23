from timeit import timeit
from random import randint, choice
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def generate_adjacency_matrix( V: int, E: int, weight_max=1):
    #   first we take all indices of lower triangle
    indices = np.tril_indices(V, -1)
    #   Since we need the "E" branches, we truncate the permuted indices
    order = np.random.permutation(len(indices[0]))[:E]
    #   Adjacency matrix consists of two triangle matrices
    branches = (np.vstack((indices[0][order], indices[1][order])),
                np.vstack((indices[1][order], indices[0][order])))
    #   Second, weights
    AMatrix = np.zeros((V, V))
    AMatrix[branches] = \
        np.tile(np.random.randint(1, weight_max+1, E ), (2, 1))
    return AMatrix

print("PART 1\n")
# number of nodes, branches, max weight
V, E, weight = 12, 50, 20
# generate weighted graph and check time of Dijkstra and Bellman-Ford
adj = generate_adjacency_matrix(V, E, weight)
# convert to NetworkX graph
G = nx.from_numpy_matrix(adj)
DijkstraAvg, BellmanFordAvg = 0,0
# loop for 5 different sources
for _ in range (5):
    src = randint(0,V-1)
    # print(f"{src} is the source node")
    BellmanFordAvg += timeit(lambda:
            nx.single_source_bellman_ford(G, src), number=10)/10
    DijkstraAvg += timeit(lambda:
            nx.single_source_dijkstra_path(G, src), number=10)/10

# check time of
print( f"Average time for Bellman-Ford algorithm  |  "
       f"{ (BellmanFordAvg/5):.6f}")
print( f"Average time for Dijkstra algorithm      |  "
       f"{ (DijkstraAvg/5):.6f}")

# Part 2

# Создайте сетку 10x10 с 30 ячейками-препятствиями.
# Выберите две случайные разрешенные ячейки и найдите кратчайший
# путь между ними, используя алгоритм A*. Повторите эксперимент
# 5 раз с другой случайной парой ячеек.


print("\nPART 2 \n")
side, num_blocks = 10, 30
G1 = nx.grid_graph([side, side])


n=0
while n<30:
    block_node = (randint(0, side - 1), randint(0, side - 1))
    if G1.has_node(block_node):
        G1.remove_node(block_node)
        n += 1


G_src = G1.copy()
times = []
pairs = []
excepts = []

for i in range(5):

    # get source and destination points
    pair = [choice(list(G_src.nodes())), None]
    G_src.remove_node(pair[0])
    pair [1] = choice(list(G_src.nodes()))
    G_src.remove_node(pair[1])

    try:
        times.append (  "%.6f" % timeit (lambda :
                nx.astar_path (G1, pair[0], pair[1]), number= 1))

    except:
        times.append("no path")

    pairs.append(pair)

    print(f"time from {pairs[i][0]} to {pairs[i][1]}  |"
          f"  {times[i]}")
