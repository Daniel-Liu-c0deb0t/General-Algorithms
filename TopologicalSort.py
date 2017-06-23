def recursive_topological_sort(u, visited, stack, graph):
    visited[u] = True
    for v in range(len(graph[u])):
        if graph[u][v] is not None and not visited[v]:
            recursive_topological_sort(v, visited, stack, graph)
    stack.append(u)


def topological_sort(graph):
    visited = [False] * len(graph)
    stack = []
    for u in range(len(graph)):
        if not visited[u]:
            recursive_topological_sort(u, visited, stack, graph)
    stack.reverse()
    return stack

print(topological_sort([[None, None, None, None, None, None],
                        [None, None, None, None, None, None],
                        [None, None, None, 1, None, None],
                        [None, 1, None, None, None, None],
                        [1, 1, None, None, None, None],
                        [1, None, 1, None, None, None]]))
