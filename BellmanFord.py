def bellman_ford_shortest_path(graph, start, end):
    dist = [None] * len(graph)
    prev = [None] * len(graph)
    dist[start] = 0
    for i in range(len(graph) - 1):
        for u in range(len(graph)):
            for v in range(len(graph)):
                if dist[u] is None or graph[u][v] is None or u == v:
                    continue
                if dist[v] is None or dist[v] > dist[u] + graph[u][v]:
                    dist[v] = dist[u] + graph[u][v]
                    prev[v] = u
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()
    return dist[end], path

print(bellman_ford_shortest_path([[None, 5, 3, 4, None],
                                  [5, None, 1, None, 2],
                                  [3, 1, None, None, None],
                                  [4, None, None, None, 4],
                                  [None, 2, None, 4, None]], 0, 4))
