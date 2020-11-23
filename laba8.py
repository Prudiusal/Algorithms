import networkx as nx
from networkx.algorithms.flow import edmonds_karp, preflow_pushы
import pandas as pd
from timeit import timeit
import random as rnd


class transport:
    def __init__(self, array: list, number_of_checks=5, display=False):
        self.V = array[0]
        self.E = array[1]
        self.min_weight = array[2]
        self.max_weight = array[3]
        self.G, self.src, self.sink = None, None, None
        self.number_of_checks = number_of_checks
        self.display = display
        self.karp_times, self.push_times, self.ratio = [], [], []
        self.measurement()


    def get_directed_weighted_graph(self):
        # create random directed graph
        self.G = None
        # print(self.counter)
        # self.counter += 1
        self.G = nx.gnm_random_graph(self.V, self.E, directed=True)
        for (u, v) in self.G.edges():
            self.G.edges[u, v]['capacity'] = rnd.randint(min_weight, max_weight)
        if self.display:
            print(f"Directed graph with {self.V} nodes and {self.E} branches was created.\n"
                  f"All branches have weights from {self.min_weight} up to {self.max_weight}.\n")


    def get_source_and_sink(self, saved_limit_src=20, saved_limit_sink=20):

        limit_src, limit_sink = saved_limit_src, saved_limit_sink

        self.src, self.sink = None, None
        i = 0

        while self.src == None or self.sink == None:

            if self.G.out_degree(i) >= limit_src and self.G.in_degree(i) == 0:
                self.src = i
                limit_src = 10000
            elif self.G.out_degree(i) == 0 and self.G.in_degree(i) >= limit_sink:
                self.sink = i
                limit_sink = 10000
            i += 1

            if i == self.V:
                if not self.src:
                    limit_src -= 1
                    if limit_src == 2:
                        break

                if not self.sink:
                    limit_sink -= 1
                    if limit_sink == 2:
                        break
                i = 0

        if self.display and self.src and self.sink:
            print(f"Source is node {self.src} with out-degree {self.G.out_degree(self.src)}")
            print(f"  Sink is node {self.sink} with in-degree  {self.G.in_degree(self.sink)}\n")


    def measurement(self):

        for i in range(self.number_of_checks):
            while not self.src or not self.sink:
                self.get_directed_weighted_graph()

                self.get_source_and_sink()

            try:
                self.karp_times.append(timeit(lambda:
                                              edmonds_karp(self.G, self.src, self.sink), number=5) / 5)
            except:
                self.karp_times.append('no path')

            try:
                self.push_times.append(timeit(lambda:
                                              preflow_push(self.G, self.src, self.sink), number=5) / 5)
            except:
                self.push_times('no path')

            try:
                self.ratio.append(self.karp_times[i] / self.push_times[i])
            except:
                self.ratio.append('----')

            self.src, self.sink = None, None
            # print(f"check number {i}")

        df = pd.DataFrame({'Edmonds-Karp': self.karp_times,
                           'Preflow Push': self.push_times,
                           'Karp/Preflow': self.ratio})

        print(f"\n\t\tTable for {self.V} nodes & {self.E} edges.\n"
              f"The capacities of edges have been distributed from {self.min_weight}"
              f" up to {self.max_weight}.")
        print(df)

if __name__ == "__main__":
    # Parameters
    V, E = 120, 200
    min_weight, max_weight = 1, 200
    number_of_checks = 5

    #            V,   R, min, max
    iters = {1: [100, 2000, 1, 1000],
             2: [100, 2000, 1, 1000],
             3: [100, 120, 500000, 1000000],
             4: [100, 120, 1, 1000],
             5: [100, 2000, 500000, 1000000]}


    for i in range(1, len(iters) + 1):
        transport(iters[i])
