class UnionFind:
    sets = []

    def __init__(self, num_sets):
        for i in range(num_sets):
            self.sets.append([i, 0])

    def add(self, i):
        self.sets.append([i, 0])

    def find(self, i):
        if self.sets[i][0] != i:
            self.sets[i][0] = self.find(self.sets[i][0])
        return self.sets[i][0]

    def union(self, i, j):
        i_root = self.find(i)
        j_root = self.find(j)
        if self.sets[i_root][1] < self.sets[j_root][1]:
            self.sets[i_root][0] = j_root
        elif self.sets[i_root][1] > self.sets[j_root][1]:
            self.sets[j_root][0] = i_root
        else:
            self.sets[j_root][0] = i_root
            self.sets[i_root][1] += 1


def kruskal_mst(graph):
    edges = []
    for i in range(len(graph)):
        for j in range(len(graph)):
            if i != j and graph[i][j] is not None:
                edges.append((graph[i][j], i, j))
    edges.sort()
    mst = []
    total_weight = 0
    uf = UnionFind(len(graph))
    i, e = 0, 0
    while e < len(graph) - 1:
        if i >= len(edges):
            return None
        weight, u, v = edges[i]
        set1 = uf.find(u)
        set2 = uf.find(v)
        if set1 != set2:
            mst.append((u, v))
            total_weight += weight
            uf.union(set1, set2)
            e += 1
        i += 1
    return total_weight, mst

print(kruskal_mst([[None, 5, 3, 4, None],
                   [5, None, 1, None, 2],
                   [3, 1, None, None, None],
                   [4, None, None, None, 4],
                   [None, 2, None, 4, None]]))
