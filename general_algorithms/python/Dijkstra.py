from heapq import heappush, heappop


def dijkstra_shortest_path(graph, start, end):
    dist = [None] * len(graph)
    pq = [(0, start, None)]
    prev = [None] * len(graph)
    while pq:
        u_dist, u, u_prev = heappop(pq)
        if dist[u] is None:
            dist[u] = u_dist
            prev[u] = u_prev
            for v in range(len(graph[u])):
                if graph[u][v] is not None and dist[v] is None:
                    heappush(pq, (u_dist + graph[u][v], v, u))
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()
    return dist[end], path

print(dijkstra_shortest_path([[None, 5, 3, 4, None],
                              [5, None, 1, None, 2],
                              [3, 1, None, None, None],
                              [4, None, None, None, 4],
                              [None, 2, None, 4, None]], 0, 4))
