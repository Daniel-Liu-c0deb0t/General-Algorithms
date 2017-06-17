def knapsack_unbounded(w, weights, values, dp):
    if dp[w] != None:
        return dp[w]
    maxVal = 0
    for i in range(len(weights)):
        if weights[i] <= w:
            maxVal = max(maxVal, values[i] + knapsack_unbounded(w - weights[i], weights, values, dp))
    dp[w] = maxVal
    return dp[w]


def knapsack01(i, w, weights, values, dp):
    if i < 0:
        return 0
    if dp[i][w] != None:
        return dp[i][w]
    if w < weights[i]:
        dp[i][w] = knapsack01(i - 1, w, weights, values, dp)
    else:
        dp[i][w] = max(knapsack01(i - 1, w, weights, values, dp), values[i] + knapsack01(i - 1, w - weights[i], weights, values, dp))
    return dp[i][w]

print(knapsack01(2, 3, [1, 2, 3], [1, 2, 4], [[None for j1 in range(4)] for i1 in range(3)]))
print(knapsack_unbounded(3, [1, 2, 3], [3, 2, 1], [None for i2 in range(4)]))
