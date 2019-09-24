import graph

def random_max_cut_ising(n):
    if n % 1:
        raise Exception("number of vertices must be even")
    g = graph.random_d_regular_graph(n, 3)
    edges = {}
    for v in g:
        for adj_v in g[v]:
            if v < adj_v:
                edges[(v, adj_v)] = 1
    return edges