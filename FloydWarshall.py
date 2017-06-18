def floyd_warshall_all_pairs_shortest_path(graph, start, end):
    dp = [[num for num in row] for row in graph]
    next = [[None if graph[row][col] is None else col for col in range(len(graph))] for row in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph)):
            if dp[j][i] is None:
                continue
            for k in range(len(graph)):
                if dp[i][k] is None or j == k:
                    continue
                if dp[j][k] is None or dp[j][k] > dp[j][i] + dp[i][k]:
                    dp[j][k] = dp[j][i] + dp[i][k]
                    next[j][k] = next[j][i]
    path = []
    curr = start
    while curr is not None:
        path.append(curr)
        curr = next[curr][end]
    return 0 if dp[start][end] is None else dp[start][end], path

print(floyd_warshall_all_pairs_shortest_path([[None, 5, 3, 4, None],
                                              [5, None, 1, None, 2],
                                              [3, 1, None, None, None],
                                              [4, None, None, None, 4],
                                              [None, 2, None, 4, None]], 0, 4))
