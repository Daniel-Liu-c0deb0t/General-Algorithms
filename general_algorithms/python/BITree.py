class BITree:
    def __init__(self, tree):
        self.bit = [0] * (len(tree) + 1)
        for i in range(len(tree)):
            self.add(i, tree[i])

    def add(self, i, val):
        i += 1
        while i < len(self.bit):
            self.bit[i] += val
            i += i & (-i)

    def sum(self, i):
        res = 0
        i += 1
        while i > 0:
            res += self.bit[i]
            i -= i & (-i)
        return res

    def get(self, i):
        return self.sum(i) - self.sum(i - 1)

    def set(self, i, val):
        self.add(i, val - self.get(i))

    def range_sum(self, i, j):
        return self.sum(j) - self.sum(i - 1)

bit = BITree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(bit.sum(9))
bit.add(2, 3)
print(bit.sum(9))
print(bit.get(2))
bit.set(2, 3)
print(bit.sum(9))
print(bit.range_sum(0, 5))
