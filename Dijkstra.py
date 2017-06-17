from heapq import heappush, heappop


def dijkstra_shortest_path(graph, start, end):
    dist = [None] * len(graph)
    pq = [(0, start)]
    prev = [-1] * len(graph)
    while pq:
        u_dist, u = heappop(pq)
        if dist[u] is None:
            dist[u] = u_dist
            for v in range(len(graph[u])):
                if graph[u][v] is not None and dist[v] is None:
                    heappush(pq, (u_dist + graph[u][v], v))
                    prev[v] = u
    path = []
    curr = end
    while curr != -1:
        path.insert(0, curr)
        curr = prev[curr]
    return dist[end], path

print(dijkstra_shortest_path([[None, 2, 4], [None, None, 1], [None, None, None]], 0, 2))
