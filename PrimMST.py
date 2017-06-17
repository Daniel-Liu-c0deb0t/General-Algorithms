from heapq import heappush, heappop


def prim_mst(graph):
    total_weight = 0
    mst_size = 0
    connected = [None] * len(graph)
    pq = [(0, 0, None)]
    while pq:
        u_weight, u, p = heappop(pq)
        total_weight += u_weight
        connected[u] = (p, u)
        mst_size += 1
        if mst_size >= len(graph):
            break
        for v in range(len(graph[u])):
            if graph[u][v] is not None and connected[v] is None:
                heappush(pq, (graph[u][v], v, u))
    connected.remove((None, 0))
    return total_weight, connected

print(prim_mst([[None, 5, 3, 4, None],
                [5, None, 1, None, 2],
                [3, 1, None, None, None],
                [4, None, None, None, 4],
                [None, 2, None, 4, None]]))
