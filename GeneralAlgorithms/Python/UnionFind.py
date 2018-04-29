class UnionFind:
    def __init__(self, num_sets):
        self.sets = []
        self.size = num_sets
        for i in range(num_sets):
            self.sets.append([i, 0])

    def add(self, i):
        self.size += 1
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

uf = UnionFind(5)
uf.union(0, 1)
uf.union(1, 2)
uf.union(3, 4)
print(uf.find(0), uf.find(2))
print(uf.find(4))
uf.add(5)
uf.union(4, 5)
print(uf.find(5))
