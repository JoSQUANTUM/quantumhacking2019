import random

def random_d_regular_graph(n, d):
    while True:
        U = set(range(n * d))
        graph = {} 
        while len(U):
            j, k = random.sample(U, 2)
            U.remove(j)
            U.remove(k)
            if int(j / d) == int(k / d):
                break
            if not int(j / d) in graph:
                graph[int(j / d)] = []
            if not int(k / d) in graph:
                graph[int(k / d)] = []
            graph[int(j / d)].append(int(k / d))
            graph[int(k / d)].append(int(j / d))
        if len(graph) == n and all([ len(set(graph[v])) == d and v not in graph[v] for v in graph ]):
            return graph