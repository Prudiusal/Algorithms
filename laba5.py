import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue

def generate_adjacency_matrix( V: int, E: int, weight_max=1):
    #   first we take all indices of lower triangle
    indices = np.tril_indices(V, -1)
    #   Since we need the "E" branches, we truncate the permuted indices
    order = np.random.permutation(len(indices[0]))[:E]
    #   Adjacency matrix consists of two triangle matrices
    branches = (np.vstack((indices[0][order], indices[1][order])),
                np.vstack((indices[1][order], indices[0][order])))
    #   Second, we give weights to all
    #   we need to create empty matrix
    AMatrix = np.zeros((V, V))
    AMatrix[branches] = \
        np.tile(np.random.randint(1, weight_max+1, E ), (2, 1))
    return AMatrix

def get_adjacency_list(matrix):
    n = len(matrix)
    AList = dict((key, []) for key in range(n))

    for i in range(n - 1):
        for j in range(i + 1, n):
            if matrix[i][j]:
                AList[i].append(j)
                AList[j].append(i)
    return AList

def BFS(Graph, s: int, end: int ):
    # create arrays
    n = len(Graph)
    color = np.full(n,'white')
    distance = np.full(n,9999999)
    # set source color as gray and distance to zero
    color[s] = 'gray'
    distance[s] = 0
    # now I need to create queue
    NodQue = Queue()
    NodQue.put(s)
    while not NodQue.empty() :
        u = NodQue.get()
        for v in Graph[u]:
            if color[v] == 'white':
                color[v] = 'gray'
                distance[v] = distance[u] + 1
                NodQue.put(v)
                if v == end:
                    out='path between node '+ str(s) +' and node '+ \
                                str(end) +' equals '+ str(distance[v])
                    return distance[v],  out
        color[u] = 'black'
    out = 'there is no path between node ' + str(s) + ' and node ' + str(end)
    return 9999999999999, out

    # using DFS to find related components of a graph

def DFS(Graph, node):
    global vertex_list
    if node not in vertex_list:
        vertex_list.append(node)
        for i in Graph[node]:
            DFS(Graph, i)

if __name__ == "__main__":
    AdjMatrix = generate_adjacency_matrix(100, 200)
    AdjList = get_adjacency_list(AdjMatrix)
    G = nx.convert_matrix.from_numpy_matrix(AdjMatrix)
    print('adjecency matrix')
    print(AdjMatrix)
    print('adjecency list')
    print(AdjList)

    print('result of DFS')
    vertex_list = []
    DFS(AdjList, 2)
    print (vertex_list)


    txt = BFS(AdjList, 2,18)[1]

    print('result of BFS')
    print(txt)
    nx.draw(G)
    plt.show()
