from collections import deque


def breadth_first_search(graph, start, end):
    visited = [False] * len(graph)
    visited[start] = True
    prev = [None] * len(graph)
    queue = deque()
    queue.append(start)
    finished = False
    while queue and not finished:
        u = queue.popleft()
        for v in range(len(graph[u])):
            if graph[u][v] is not None and not visited[v]:
                queue.append(v)
                visited[v] = True
                prev[v] = u
                if v == end:
                    finished = True
                    break
    path = []
    curr = end
    dist = 0
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
        dist += 1
    path.reverse()
    return dist, path

print(breadth_first_search([[None, 1, 1, 1, None],
                            [1, None, 1, None, 1],
                            [1, 1, None, None, None],
                            [1, None, None, None, 1],
                            [None, 1, None, 1, None]], 0, 4))
